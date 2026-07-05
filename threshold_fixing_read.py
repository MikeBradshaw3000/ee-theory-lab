#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Threshold-fixing pure read v3 (second defect repair; per the L2-arbitrated repair protocol)
REPAIR 2 SCOPE: the onset meanI control construction only. v2 permuted CELLS WITHIN TICKS
(argsort axis=1 — the committed z-score convention, a per-tick spatial shuffle), while the spec's
operative meanI control is the PER-CELL INDEPENDENT TIME SHUFFLE (READING_D C3; argsort axis=0).
The mislabel was CAUGHT BY L2's hardening clause: the invariance demonstration returned False,
which is impossible under the labeled control (a permutation cannot change a time-mean).
The axis fix consumes no RNG: identical rand arrays in identical order, so ALL other emissions —
including onset meanI RAW, both persistence series, and repair-1's corrected g3_rho_match —
must reproduce bit-identically; the built-in granular audit proves it or halts.
Repair 1 (v2, L2-arbitrated): corrected 3.4 cap-separation set (discriminating tier strata only).
Same committed inputs, same READ_RNG_SEED = 20260704, throughout.
NON-SEEDING PURE READ; emits cycle3/data_out/threshold_fixing_read_results.json.

Apparatus functions calculate_morans_i_toroidal_8, batch_morans_i_toroidal_8, and
get_neighbor_count are copied BYTE-FOR-BYTE from the committed c3_w2_rule_c_m2.py.
"""

import sys, os, json, hashlib
import numpy as np

# ==========================================
# Fixed read constants (recorded in JSON)
# ==========================================
READ_RNG_SEED = 20260704          # frozen read-control RNG seed; no-rerun discipline
PERMUTATIONS = 199                # committed convention
QUANTILE_METHOD = "lower"         # non-interpolating empirical order statistic, everywhere
GRID_SIZE = 50
LAMBDA = 0.40
S_SURV = 0.40                     # Lambda-only survival at the anchor
SEEDS = [42, 137, 256, 1024, 31415]
BLOCK = 25
PRIMARY_BLOCKS = list(range(3, 15))            # blocks 3-14 inclusive (12 blocks)
PRIMARY_WINDOW_STARTS = [75 + 25*i for i in range(9)]   # ticks 75..275 (window starts at blocks 3-11)
M_WINDOW_STARTS = [0, 25, 50, 75, 100]         # committed M2 window family
WINDOW_LEN = 100
DATA = os.path.join("cycle3", "data_out")

# c-label -> kappa at Lambda=0.40 (committed M2 map); (label, kappa, npz kstr)
CELLS = [
    ( 0.00,  0.0000, "kp0_0000"),
    (+0.05, +0.1042, "kp0_1042"), (-0.05, -0.1042, "km0_1042"),
    (+0.10, +0.2090, "kp0_2090"), (-0.10, -0.2090, "km0_2090"),
    (+0.20, +0.4221, "kp0_4221"), (-0.20, -0.4221, "km0_4221"),
    (+0.35, +0.7599, "kp0_7599"), (-0.35, -0.7599, "km0_7599"),
]
RESPONSIVE = [c for c in CELLS if abs(c[0]) >= 0.20]
U_TIERS = [0.10, 0.25, 0.50]                   # contract Section 3
SCHEDULE_LEVELS = sorted({0.0} | {u/2 for u in U_TIERS} | set(U_TIERS))  # construction-only

# ==========================================
# Byte-for-byte apparatus copies (committed c3_w2_rule_c_m2.py)
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
# Helpers
# ==========================================

def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))

LOGIT_L = float(np.log(LAMBDA / (1.0 - LAMBDA)))

def reconstruct_p_become(states_tick, kappa, u_level=0.0):
    """p_become(t) from states[t]: the field that would update t -> t+1.
    No random draw is made; no state is advanced. (Spec 3.3 tick alignment.)"""
    q = get_neighbor_count(states_tick) / 8.0
    return sigmoid(LOGIT_L + u_level + kappa * (2.0 * q - 1.0))

def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def q_lower(vals, q):
    """Non-interpolating empirical order statistic, method='lower'."""
    return float(np.percentile(np.asarray(vals, dtype=float), q, method=QUANTILE_METHOD))

def load_states(path, expect_ticks):
    arr = np.load(path)["states"]
    if arr.shape != (expect_ticks, GRID_SIZE, GRID_SIZE):
        raise RuntimeError(f"FAIL CLOSED: {path} shape {arr.shape} != ({expect_ticks},{GRID_SIZE},{GRID_SIZE})")
    return arr

def solve_rho_star(u_level, kappa, iters=500, damp=0.5):
    """Self-consistent mean-field fixed point (spec 3.8): p_eff depends on rho via q=rho."""
    rho = 0.40
    for _ in range(iters):
        p = sigmoid(LOGIT_L + u_level + kappa * (2.0 * rho - 1.0))
        rho_new = p / (1.0 - S_SURV + p)
        rho = damp * rho_new + (1.0 - damp) * rho
    return float(rho)

# ==========================================
# Main
# ==========================================

def main():
    if sys.prefix == sys.base_prefix:
        raise RuntimeError("PRE-FLIGHT FAIL: Virtual environment is not active.")

    results = {"read_constants": {
        "READ_RNG_SEED": READ_RNG_SEED, "PERMUTATIONS": PERMUTATIONS,
        "quantile_method": QUANTILE_METHOD, "residue_definition": "abs(raw_stat - mean_control_stat)",
        "controls": {"Psi_meanI_state": "per-cell independent time-shuffle",
                     "Psi_persistence_I": "spatial permutation of persistence grid (committed compute_persistence_null convention)"},
        "primary_blocks": PRIMARY_BLOCKS, "primary_window_starts_ticks": PRIMARY_WINDOW_STARTS,
        "no_rerun_discipline": "This read may not be rerun with a different control seed to move thresholds.",
    }}

    # ---- Input manifest, fail closed (spec Section 1 / item 12) ----
    manifest = {"family_F": [], "family_M": [], "F3_status": "F3 bit-exact 5/5 (session record 2026-07-04)"}
    F_states = {}
    for seed in SEEDS:
        p = os.path.join(DATA, f"c3_w2_null_extension_states_L0.4_kp0_0000_s{seed}.npz")
        if not os.path.exists(p):
            raise RuntimeError(f"FAIL CLOSED: missing Family F input {p}")
        F_states[seed] = load_states(p, 400)
        manifest["family_F"].append({"file": os.path.basename(p), "shape": [400, 50, 50], "sha256": sha256_of(p)})
    M_states = {}
    for (c, kappa, kstr) in CELLS:
        for seed in SEEDS:
            p = os.path.join(DATA, f"c3_w2_rule_c_m2_states_L0.4_{kstr}_s{seed}.npz")
            if not os.path.exists(p):
                raise RuntimeError(f"FAIL CLOSED: missing Family M input {p}")
            M_states[(c, seed)] = load_states(p, 200)
            manifest["family_M"].append({"file": os.path.basename(p), "shape": [200, 50, 50], "sha256": sha256_of(p)})
    try:
        manifest["read_script_sha256"] = sha256_of(os.path.abspath(__file__))
    except Exception:
        manifest["read_script_sha256"] = "unavailable"
    results["input_manifest"] = manifest

    # ---- 3.8 first (its solutions feed the 3.4 cap and 3.6 envelope) ----
    fixed_points = {}
    for (c, kappa, _) in CELLS:
        for lvl in SCHEDULE_LEVELS:
            fixed_points[(c, round(lvl, 4))] = solve_rho_star(lvl, kappa)
    tier_bands = {}   # (tier_label, c) -> [lo, hi] over the tier's three schedule levels
    for u in [0.0] + U_TIERS:
        levels = [0.0] if u == 0.0 else [0.0, u/2, u]
        for (c, kappa, _) in CELLS:
            vals = [fixed_points[(c, round(l, 4))] for l in levels]
            tier_bands[(round(u, 2), c)] = [min(vals), max(vals)]

    # ---- 3.1 G1 floor imprint null (Family F, blocks 3-14) ----
    template_base = np.array([0.0, 0.5, 1.0]) - 0.5
    r_vals, beta_vals, cov_vals = [], [], []
    F_block_means = {}
    for seed in SEEDS:
        rhos = F_states[seed].reshape(400, -1).mean(axis=1)
        bm = np.array([rhos[b*BLOCK:(b+1)*BLOCK].mean() for b in PRIMARY_BLOCKS])  # 12 values
        F_block_means[seed] = bm
        for phi in range(3):
            tmpl = np.roll(np.tile(template_base, 4), phi)
            cov = float(np.mean((bm - bm.mean()) * (tmpl - tmpl.mean())))
            var_t = float(np.var(tmpl))
            beta = cov / var_t
            denom = float(np.std(bm) * np.std(tmpl))
            r = cov / denom if denom > 1e-15 else 0.0
            r_vals.append(r); beta_vals.append(beta); cov_vals.append(cov)
    results["g1_imprint"] = {
        "r_values": r_vals, "beta_values": beta_vals, "cov_values_diagnostic": cov_vals,
        "correlation_threshold": max(0.0, max(r_vals)),
        "slope_amplitude_threshold": max(0.0, max(beta_vals)),
        "r_mean_sd_descriptive": [float(np.mean(r_vals)), float(np.std(r_vals))],
        "beta_mean_sd_descriptive": [float(np.mean(beta_vals)), float(np.std(beta_vals))],
        "apparatus_limit": ("COARSE NULL: 3-block period over the 12-block primary set admits exactly 3 "
                            "integer phase alignments -> 15 pooled seed-phase values; thresholds are the "
                            "conservative MAX, not a percentile. Recorded as an apparatus limit."),
    }

    # ---- 3.2 G1 floor overdispersion null ----
    variances = [float(np.var(F_block_means[s]))  # ddof=0 (np.var default)
                 for s in SEEDS]
    results["g1_overdispersion"] = {
        "seed_variances_ddof0": variances,
        "floor_overdispersion_threshold": max(variances),
        "mean_sd_descriptive": [float(np.mean(variances)), float(np.std(variances))],
        "scope_note": ("Necessary, not sufficient, for G1b. Does NOT substitute for the full 135-row "
                       "CM-0 comparator dominance rule (separate predeclared relation, evaluated after "
                       "CM-0 exists). No result may say 'above CM-0' from this floor threshold alone."),
    }

    # ---- 3.3 G2 activation anchor + 3.6 G4 compression (one reconstruction pass) ----
    g2 = {}
    g4_perticks = {"mean_slope": [], "q05_slope": [], "tail_mass": []}
    g4_by_cell = {}
    for (c, kappa, kstr) in CELLS:
        per_seed_propI, per_seed_propI_masked = [], []
        cell_slopes = {"mean_slope": [], "q05_slope": [], "tail_mass": [],
                       "p_min": [], "p_max": [], "mean_p": []}
        for seed in SEEDS:
            st = M_states[(c, seed)]
            tick_Is, tick_Is_masked = [], []
            for t in range(200):
                pb = reconstruct_p_become(st[t], kappa)
                tick_Is.append(calculate_morans_i_toroidal_8(pb))
                # inactive-cell-masked DIAGNOSTIC: active cells mean-imputed with inactive-cell mean
                inact = (st[t] == 0)
                if inact.any() and (~inact).any():
                    pm = pb.copy(); pm[~inact] = pb[inact].mean()
                    tick_Is_masked.append(calculate_morans_i_toroidal_8(pm))
                else:
                    tick_Is_masked.append(0.0)
                sl = pb * (1.0 - pb)
                cell_slopes["mean_slope"].append(float(sl.mean()))
                cell_slopes["q05_slope"].append(q_lower(sl.ravel(), 5))
                cell_slopes["tail_mass"].append(float(np.mean((pb < 0.05) | (pb > 0.95))))
                cell_slopes["p_min"].append(float(pb.min()))
                cell_slopes["p_max"].append(float(pb.max()))
                cell_slopes["mean_p"].append(float(pb.mean()))
            per_seed_propI.append(float(np.mean(tick_Is)))
            per_seed_propI_masked.append(float(np.mean(tick_Is_masked)))
        key = f"c={c:+.2f}"
        g2[key] = {"per_seed_propI": per_seed_propI,
                   "mean": float(np.mean(per_seed_propI)),
                   "median": float(np.median(per_seed_propI)),
                   "min": float(np.min(per_seed_propI)),
                   "lower10_method_lower": q_lower(per_seed_propI, 10),
                   "masked_diagnostic_per_seed": per_seed_propI_masked,
                   "masked_diagnostic_note": ("Diagnostic only (active cells mean-imputed with inactive-cell "
                                              "mean before Moran). Never replaces the full-surface gate.")}
        g4_by_cell[key] = {k: {"mean": float(np.mean(v)), "min": float(np.min(v)), "max": float(np.max(v))}
                           for k, v in cell_slopes.items()}
        if abs(c) >= 0.20:
            for k in ("mean_slope", "q05_slope", "tail_mass"):
                g4_perticks[k].extend(cell_slopes[k])
    results["g2_anchor"] = {
        "gate_note": "Full-surface prop_I is the gate anchor (contract decomposition read).",
        "activation_floor_pos": g2["c=+0.35"]["lower10_method_lower"],
        "activation_floor_neg": g2["c=-0.35"]["lower10_method_lower"],
        "sign_separation_note": "Signs reported separately before any sign-symmetry summary; trend per tier/per sign/across seeds; never sign-pooled.",
        "cells": g2,
    }
    # ---- 3.6 constants + planned-drive envelope ----
    envelope = {}
    for lvl in SCHEDULE_LEVELS:
        for (c, kappa, _) in CELLS:
            p0 = float(sigmoid(LOGIT_L + lvl - abs(kappa)))
            p1 = float(sigmoid(LOGIT_L + lvl + abs(kappa)))
            viol = bool(p0 < 0.05 or p1 > 0.95 or p1 < 0.05 or p0 > 0.95)
            envelope[f"level={lvl:.3f},c={c:+.2f}"] = {"p_env": [min(p0, p1), max(p0, p1)], "violates_hard_interval": viol}
    any_env_violation = any(v["violates_hard_interval"] for v in envelope.values())
    results["g4_compression"] = {
        "constants": {
            "mean_slope_floor_lower10": q_lower(g4_perticks["mean_slope"], 10),
            "q05_slope_floor_lower10": q_lower(g4_perticks["q05_slope"], 10),
            "tail_mass_ceiling_max_observed": float(np.max(g4_perticks["tail_mass"])),
            "hard_interval": [0.05, 0.95],
            "constants_scope": "Per-tick distributions pooled over responsive cells |c|>=0.20, both signs, all seeds, all 200 ticks.",
        },
        "per_cell_summary": g4_by_cell,
        "planned_drive_envelope": envelope,
        "pre_seed_compression_risk": any_env_violation,
        "rule": "A CM-1 row passes G4 only on all three criteria; mean slope alone never sufficient.",
    }

    # ---- 3.4 G3 rho-match scale ----
    F_window_means = []
    for seed in SEEDS:
        rhos = F_states[seed].reshape(400, -1).mean(axis=1)
        F_window_means.extend(float(rhos[ws:ws+WINDOW_LEN].mean()) for ws in PRIMARY_WINDOW_STARTS)
    sigma_window_F = float(np.std(F_window_means))  # ddof=0
    cell_vars = []
    for (c, kappa, _) in CELLS:
        wms = []
        for seed in SEEDS:
            rhos = M_states[(c, seed)].reshape(200, -1).mean(axis=1)
            wms.extend(float(rhos[ws:ws+WINDOW_LEN].mean()) for ws in M_WINDOW_STARTS)
        cell_vars.append(float(np.var(wms)))
    sigma_window_M = float(np.sqrt(np.mean(cell_vars)))
    sigma_rho_match = max(sigma_window_F, sigma_window_M)
    provisional = 2.0 * sigma_rho_match
    # CORRECTED cap-separation set (L2-arbitrated defect repair, 2026-07-05):
    # The cap is computed ONLY from construction-predicted rho separations between strata the
    # planned read must keep DISTINGUISHABLE — adjacent common-mode tier/schedule-level rho
    # strata at the SAME c label and sign (bins wider than those would merge distinct rho-lift
    # strata). EXCLUDED: same-tier cross-c and cross-sign near-degenerate pairs (including +c
    # vs -c and small-|c| neighbors) — those are candidate matched-rho TARGETS, not strata to
    # discriminate. The v1 rule min-ed over all pairs and collapsed the cap; that JSON is invalid.
    tiers_sorted = [0.0] + U_TIERS
    sep_set = []
    for (c, kappa, _) in CELLS:
        mids = []
        for u in tiers_sorted:
            b = tier_bands[(round(u, 2), c)]
            mids.append(((b[0] + b[1]) / 2.0, u))
        for i in range(len(mids) - 1):
            d = abs(mids[i + 1][0] - mids[i][0])
            if d > 1e-12:
                sep_set.append({"c": c, "tiers": [mids[i][1], mids[i + 1][1]], "sep": float(d)})
    sep_discrim_min = float(min(s["sep"] for s in sep_set))
    cap = 0.5 * sep_discrim_min
    cap_bound = bool(provisional > cap)
    delta_rho_match = float(min(provisional, cap)) if cap_bound else float(provisional)
    results["g3_rho_match"] = {
        "unit": "window-mean rho of eligible primary windows",
        "sigma_window_F": sigma_window_F, "sigma_window_M": sigma_window_M,
        "sigma_rho_match": sigma_rho_match, "provisional_2x": provisional,
        "cap_separation_set": sep_set,
        "excluded_pair_classes": ("Same-tier cross-c and cross-sign pairs (incl. +c vs -c and small-|c| "
                                  "neighbors): candidate matched-rho targets, not strata to discriminate."),
        "sep_discrim_min": sep_discrim_min, "cap_half_sep_discrim_min": cap,
        "cap_bound": cap_bound, "Delta_rho_match": delta_rho_match,
        "repair_note": "v2 corrected cap rule (L2-arbitrated defect repair); v1 JSON invalid, preserved as *_INVALID_v1.json.",
        "note": "Setting-level mean difference below Delta_rho_match is descriptive only; never replaces bin-level common support.",
    }

    # ---- 3.5 G3 bin-eligibility constants (structural) ----
    results["g3_bin_eligibility"] = {
        "N_bin_min": 9, "S_bin_min": 3,
        "no_single_seed_dominance": "No single seed may contribute more than half of qualifying windows on either side.",
        "phase_rule": ("Comparison is phase-stratified, OR both sides' window-start phase histograms over the three "
                       "schedule phases match within one window per phase; enough-windows-but-phase-confounded bins "
                       "are reported as common-support-present-but-phase-confounded and excluded from ordering claims."),
        "derivation": "9 primary windows/seed x 5 seeds = 45 instances/setting; N_bin_min = one complete primary-window-family equivalent.",
    }

    # ---- 3.7 Onset null (axis-specific controls; frozen RNG) ----
    np.random.seed(READ_RNG_SEED)
    raw_meanI, res_meanI, raw_pers, res_pers = [], [], [], []
    invariance_checked = False
    invariance_holds = None
    for seed in SEEDS:                    # fixed documented order: seeds asc, windows asc
        st = F_states[seed]
        for ws in PRIMARY_WINDOW_STARTS:
            win = st[ws:ws+WINDOW_LEN]
            # raw statistics
            tick_Is = batch_morans_i_toroidal_8(win)
            rmI = float(np.mean(tick_Is))
            pgrid = np.mean(win, axis=0)
            rpI = float(calculate_morans_i_toroidal_8(pgrid))
            raw_meanI.append(abs(rmI)); raw_pers.append(abs(rpI))
            # meanI control: PER-CELL INDEPENDENT TIME SHUFFLE (spec v2.1 / READING_D C3 construction).
            # v2 DEFECT: argsort(axis=1) permuted cells within ticks (per-tick spatial shuffle) — the
            # committed z-convention, NOT the spec's operative control. Corrected: axis=0 permutes
            # ticks independently per cell. Same rand array shapes/order -> RNG stream unchanged.
            flat = win.reshape(WINDOW_LEN, -1)
            null_meanIs = np.zeros(PERMUTATIONS)
            for p in range(PERMUTATIONS):
                rand_idx = np.random.rand(WINDOW_LEN, GRID_SIZE*GRID_SIZE).argsort(axis=0)
                shuffled = np.take_along_axis(flat, rand_idx, axis=0).reshape(WINDOW_LEN, GRID_SIZE, GRID_SIZE)
                null_meanIs[p] = np.mean(batch_morans_i_toroidal_8(shuffled))
                if not invariance_checked:
                    # hardening clause: per-cell time shuffle must preserve the persistence grid exactly
                    invariance_holds = bool(np.allclose(np.mean(shuffled, axis=0), pgrid))
                    invariance_checked = True
            res_meanI.append(abs(rmI - float(np.mean(null_meanIs))))
            # persistence control: spatial permutation of the persistence grid (committed convention)
            flat_p = pgrid.flatten()
            null_pIs = np.zeros(PERMUTATIONS)
            for p in range(PERMUTATIONS):
                shuf = np.random.permutation(flat_p).reshape((GRID_SIZE, GRID_SIZE))
                null_pIs[p] = calculate_morans_i_toroidal_8(shuf)
            res_pers.append(abs(rpI - float(np.mean(null_pIs))))
    def onset_axis(raws, resids):
        return {"raw_values": raws, "residue_values": resids,
                "raw_p97_5_method_lower": q_lower(raws, 97.5), "raw_max": float(np.max(raws)),
                "residue_p97_5_method_lower": q_lower(resids, 97.5), "residue_max": float(np.max(resids))}
    results["onset_null"] = {
        "Psi_meanI_state": onset_axis(raw_meanI, res_meanI),
        "Psi_persistence_I": onset_axis(raw_pers, res_pers),
        "controls": results["read_constants"]["controls"],
        "time_shuffle_persistence_invariance": {
            "algebraically_zero": True, "demonstrated_numerically": invariance_holds,
            "note": "Per-cell time shuffle preserves each cell's time mean; persistence grid preserved exactly; diagnostic-only, never the operative persistence residue gate."},
        "operative_floor_conditional": ("MAX-OBSERVED is the operative per-window onset floor (raw and residue, per axis) "
                                        "until the setting-level earned-window rule is verified for the 9-window primary "
                                        "family; the 97.5th-percentile values travel alongside for when that verification lands."),
    }

    # ---- 3.8 Feasibility classification ----
    buffer = delta_rho_match + sigma_rho_match
    def overlap_len(b1, b2):
        return min(b1[1], b2[1]) - max(b1[0], b2[0])
    pairs_a, pairs_b = [], []
    for (t1, c1), b1 in tier_bands.items():
        for (t2, c2), b2 in tier_bands.items():
            if (t1, c1) >= (t2, c2):
                continue
            ol = overlap_len(b1, b2)
            entry = {"cell_1": [t1, c1], "cell_2": [t2, c2], "bands": [b1, b2], "overlap": ol}
            if (c1 == 0.0 and t1 > 0 and abs(c2) >= 0.20) or (c2 == 0.0 and t2 > 0 and abs(c1) >= 0.20):
                pairs_a.append(entry)
            if c1 != c2 and (abs(c1) >= 0.20 or abs(c2) >= 0.20):
                pairs_b.append(entry)
    def classify(pairs):
        if any(p["overlap"] > buffer for p in pairs):
            return "feasible"
        if any(p["overlap"] > -buffer for p in pairs):
            return "indeterminate"
        return "not_feasible"
    cls_a, cls_b = classify(pairs_a), classify(pairs_b)
    order = {"not_feasible": 0, "indeterminate": 1, "feasible": 2}
    overall = min([cls_a, cls_b], key=lambda k: order[k])
    results["feasibility_audit"] = {
        "method": "Self-consistent mean-field fixed point rho* = p_eff(rho*)/(1-s+p_eff(rho*)), q=rho*, damped iteration.",
        "fixed_points": {f"c={c:+.2f},level={l:.3f}": v for (c, l), v in fixed_points.items()},
        "tier_bands": {f"tier={t:.2f},c={c:+.2f}": b for (t, c), b in tier_bands.items()},
        "buffer": buffer,
        "path_a_classification": cls_a, "path_b_classification": cls_b,
        "overall_classification": overall,
        "path_a_best_pairs": sorted(pairs_a, key=lambda p: -p["overlap"])[:5],
        "path_b_best_pairs": sorted(pairs_b, key=lambda p: -p["overlap"])[:5],
        "rule": ("not_feasible or indeterminate halts automatic seedability and routes to Mike; never worked around "
                 "by relaxing G3 after output. feasible is necessary, not sufficient."),
        "cm0_static_note": "CM-0 static levels audited at u/2 provisional (solved-offset rule pending its own pre-seed calculation).",
    }

    out = os.path.join(DATA, "threshold_fixing_read_results.json")
    with open(out, "w") as f:
        json.dump(results, f, indent=1)
    print(f"WROTE {out}")

    # ---- L2-protocol repair-isolation audit (v3, granular) against the invalid v2 JSON ----
    v2_path = os.path.join(DATA, "threshold_fixing_read_results_INVALID_v2.json")
    if os.path.exists(v2_path):
        with open(v2_path) as f:
            prev = json.load(f)
        def same(a, b):
            return json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True)
        audit_ok = True
        for key in ["g1_imprint", "g1_overdispersion", "g2_anchor", "g4_compression", "g3_rho_match"]:
            ok = same(prev.get(key), results.get(key))
            print(f"AUDIT {key}: {'UNCHANGED' if ok else 'CHANGED  <-- AUDIT FAIL'}")
            audit_ok = audit_ok and ok
        po, no = prev.get("onset_null", {}), results.get("onset_null", {})
        checks = [
            ("onset meanI RAW", same(po.get("Psi_meanI_state", {}).get("raw_values"), no.get("Psi_meanI_state", {}).get("raw_values"))),
            ("onset persistence RAW", same(po.get("Psi_persistence_I", {}).get("raw_values"), no.get("Psi_persistence_I", {}).get("raw_values"))),
            ("onset persistence RESIDUE", same(po.get("Psi_persistence_I", {}).get("residue_values"), no.get("Psi_persistence_I", {}).get("residue_values"))),
        ]
        for name, ok in checks:
            print(f"AUDIT {name}: {'UNCHANGED' if ok else 'CHANGED  <-- AUDIT FAIL'}")
            audit_ok = audit_ok and ok
        def npz_digests(m):
            return json.dumps([e for fam in ("family_F", "family_M") for e in m.get(fam, [])], sort_keys=True)
        man_same = npz_digests(prev.get("input_manifest", {})) == npz_digests(results.get("input_manifest", {}))
        print(f"AUDIT input NPZ digests: {'UNCHANGED' if man_same else 'CHANGED  <-- AUDIT FAIL'}")
        audit_ok = audit_ok and man_same
        inv = results["onset_null"]["time_shuffle_persistence_invariance"]["demonstrated_numerically"]
        print(f"AUDIT onset meanI RESIDUE: EXPECTED CHANGED (the repair target)")
        print(f"AUDIT invariance demonstration: {'True (corrected control confirmed)' if inv else 'False  <-- AUDIT FAIL: control still wrong'}")
        audit_ok = audit_ok and bool(inv)
        if audit_ok:
            print("REPAIR-ISOLATION AUDIT v3: PASS — repair isolated to the meanI control; invariance holds under the corrected construction.")
        else:
            print("REPAIR-ISOLATION AUDIT v3: FAIL — HALT; route to Mike. Do not freeze this JSON.")
    else:
        print("AUDIT SKIPPED: threshold_fixing_read_results_INVALID_v2.json not found — rename the v2 JSON before running.")

    print(f"G1: r_thresh={results['g1_imprint']['correlation_threshold']:.4f}  beta_thresh={results['g1_imprint']['slope_amplitude_threshold']:.6f}")
    print(f"G1 overdisp threshold={results['g1_overdispersion']['floor_overdispersion_threshold']:.8f}")
    print(f"G2 floors: pos={results['g2_anchor']['activation_floor_pos']:.4f}  neg={results['g2_anchor']['activation_floor_neg']:.4f}")
    print(f"G3 Delta_rho_match={delta_rho_match:.5f} (cap_bound={cap_bound})")
    print(f"G4 mean_slope_floor={results['g4_compression']['constants']['mean_slope_floor_lower10']:.4f}  tail_ceiling={results['g4_compression']['constants']['tail_mass_ceiling_max_observed']:.4f}  pre_seed_risk={any_env_violation}")
    om = results['onset_null']
    print(f"Onset meanI: raw_max={om['Psi_meanI_state']['raw_max']:.5f} res_max={om['Psi_meanI_state']['residue_max']:.5f}")
    print(f"Onset pers:  raw_max={om['Psi_persistence_I']['raw_max']:.5f} res_max={om['Psi_persistence_I']['residue_max']:.5f}")
    print(f"Feasibility: path_a={cls_a}  path_b={cls_b}  OVERALL={overall}")

if __name__ == "__main__":
    main()
