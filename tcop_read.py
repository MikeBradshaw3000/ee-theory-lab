#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TCOP READ v2 — pure read of the committed two-channel ordering probe dataset.
Governed by: TCOP_READ_SPEC.md (CANONICAL, Mike-arbitrated A1-A5 2026-07-06) +
TCOP_READ_SPEC_AMENDMENT_1.md (CANONICAL, Mike-arbitrated B1 option (i) 2026-07-06),
contract 8c94d8c, addendum 8a777e6. L1-drafted; no Layer 3.

v2 CHANGELOG (L2 hostile build review, reject-as-execution-ready -> all folded):
 B1 (blocker; Amendment 1): path-(a) risky-form failure now requires, jointly:
     the global Section 3.2 setting flag, verified lift (strict-all), AND onset
     evidence represented in >=1 G3-ELIGIBLE path-(a) bin from gate-passing rows.
     Sentinel c=0 events tagged G3_eligible; global flag alone never sufficient.
 D1: every global rho bin over [0.35, 0.55) is evaluated for every pair/axis;
     bins empty on both sides are reported compactly as an out-of-support index
     list (bins_empty_out_of_support) rather than one record each (disclosed N7).
 D2: exact per-run block-index set {0..15} and window-start set {0,25,...,300}
     verified, no duplicates; every CSV row's identifier columns (mode, c_label,
     kappa, tier, u_const, seed) verified against the run manifest. Fail closed.
 D3: prop_I_masked_diagnostic cross-checked like-for-like when numeric; at
     zero-variance blocks the recorded degenerate 0.0 convention is asserted.
     The column is diagnostic-only, never gate-bearing.
 D4: startup additionally verifies N_bin_min, S_bin_min, PERMUTATIONS, the hard
     interval, and the alongside p97.5 onset values against the threshold JSON.
     READ_RNG_SEED = 20260706 is SPEC-FIXED (the JSON's 20260704 is the threshold
     read's own seed; never compared).
 D5: console summary is counts-only; outcome labels are written to the JSON only.
 D6: named per-row zero_mode_diagnostics section: block-rho variance, phase-0
     schedule regression, phase-1/2 diagnostics, block-rho autocorrelation at
     lags 1/2/3. Diagnostic only; never a gate.
 C7: runtime byte-for-byte enforcement: at startup the script reads the committed
     source files and asserts each copied function's own source text appears
     VERBATIM in its committed origin (inspect.getsource containment). Fail closed.
 C1 (wording): CM-1 NPZs are hashed for the input manifest at startup; no CM-1
     NPZ is LOADED (np.load) or statistically processed before the CM-0
     comparator sets are computed and digest-frozen.

Frozen constants verified against cycle3/data_out/threshold_fixing_read_results.json
at startup (fail closed). READ_RNG_SEED = 20260706, frozen; no rerun with a
different seed to move outcomes; crash-rerun with the SAME seed is permitted.

Apparatus functions calculate_morans_i_toroidal_8, batch_morans_i_toroidal_8,
get_neighbor_count are copied BYTE-FOR-BYTE from committed c3_w2_rule_c_m2.py.
u_t_for and sanitize_float are copied byte-for-byte from committed c3_w2_tcop.py.
reconstruct_p_become follows threshold_fixing_read.py v3 (the driven-path-checked
convention): the field that would update t -> t+1; no draw; no advance.

DISCLOSED IMPLEMENTATION NOTES (recorded here and in the JSON):
 N1. Recorded block-CSV q05_slope used np.percentile DEFAULT (linear), pooled per
     block. The G4 gate quantity uses method="lower" (pooled per block; the
     operative code convention — not identical to a per-tick min-q05 rule, per
     L2's caveat, recorded). The recorded column is cross-checked like-for-like
     with the default method. No silent substitution either way.
 N2. Recorded prop_I_full_surface = 0.0 at c = 0 is the committed Moran function's
     degenerate return on a (near-)constant field. The read verifies field spatial
     variance < EPS_VAR there and records zero-variance/non-identifiable; never
     numeric in the G2 trend.
 N3. Recorded window z columns consumed ongoing run-RNG state at build time; they
     travel AS RECORDED, labeled recorded-not-reconstructed. z never gates.
 N4. Row-level onset flags (k_onset) always use all 9 primary windows (spec 3.2).
     Outcome/tracking bins use only windows from rows passing G4 and (nonzero
     tiers) G1; path-(a) failure additionally bin-qualified per Amendment 1.
 N5. Verified common-mode lift at (tier>0, c=0) = ALL five seed rows pass G1.
 N6. Iteration order: np.random.seed(READ_RNG_SEED) once; CM-0 runs sorted
     (tier, c_label, seed), then CM-1 runs sorted (tier, c_label, seed); per
     window: 199 meanI time-shuffles (argsort axis=0) then 199 persistence
     spatial permutations.
 N7. D1 compaction: empty-on-both-sides global bins reported as an index list
     with status out-of-support, not one record each (JSON economy; every bin
     is still evaluated and reported).
"""

import sys, os, json, hashlib, inspect
import numpy as np
import pandas as pd

# ==========================================
# Frozen read constants (spec Section 2)
# ==========================================
READ_RNG_SEED = 20260706          # SPEC-FIXED (not the threshold JSON's 20260704)
PERMUTATIONS = 199
QUANTILE_METHOD = "lower"
GRID_SIZE = 50
N_CELLS = GRID_SIZE * GRID_SIZE
LAMBDA = 0.40
S_SURV = 0.40
LOGIT_L = float(np.log(LAMBDA / (1.0 - LAMBDA)))
SEEDS = [42, 137, 256, 1024, 31415]
TICKS = 400
BLOCK = 25
N_BLOCKS = 16
WINDOW_LEN = 100
PRIMARY_BLOCKS = list(range(3, 15))                       # 3..14
PRIMARY_WINDOW_STARTS = [75 + 25 * i for i in range(9)]   # ticks 75..275
ALL_WINDOW_STARTS = [25 * i for i in range(13)]           # ticks 0..300
U_TIERS = [0.10, 0.25, 0.50]
KAPPA_MAP = [
    ( 0.00,  0.0000),
    (+0.05, +0.1042), (-0.05, -0.1042),
    (+0.10, +0.2090), (-0.10, -0.2090),
    (+0.20, +0.4221), (-0.20, -0.4221),
    (+0.35, +0.7599), (-0.35, -0.7599),
]
DATA = os.path.join("cycle3", "data_out")
BLOCK_CSV = os.path.join(DATA, "c3_w2_tcop_blocks.csv")
WINDOW_CSV = os.path.join(DATA, "c3_w2_tcop_windows.csv")
PREFLIGHT_JSON = os.path.join(DATA, "c3_w2_tcop_preflight.json")
THRESH_JSON = os.path.join(DATA, "threshold_fixing_read_results.json")
OUT_JSON = os.path.join(DATA, "tcop_read_results.json")
PREFLIGHT_SCRIPT_SHA = "466455f20550b8c41a984ce40db49ebe0e832ae56c269ab518b521c6ad83b7e7"
COMMITTED_M2_SRC = os.path.join("cycle3", "wave_two", "c3_w2_rule_c_m2.py")
COMMITTED_TCOP_SRC = os.path.join("cycle3", "wave_two", "c3_w2_tcop.py")

# Frozen thresholds (addendum 8a777e6; verified vs THRESH_JSON at startup)
G1_CORR = 0.7840162452332338
G1_SLOPE = 0.0026279999999999915
G1B_VAR = 4.469162666666656e-06
G2_FLOOR_POS = 0.3832176592110196
G2_FLOOR_NEG = 0.38138345899890086
DELTA_RHO = 0.002827351608578471
N_BIN_MIN = 9
S_BIN_MIN = 3
G4_MEAN_FLOOR = 0.22556575062981687
G4_Q05_FLOOR = 0.19883692760900232
G4_TAIL_CEIL = 0.0
HARD_LO, HARD_HI = 0.05, 0.95
ONSET = {  # operative MAX-OBSERVED floors (A4 Branch A); p97.5 alongside, diagnostics only
    "Psi_meanI_state":    {"raw": 0.001990247078984684,  "res": 0.0021133919208696263,
                           "raw_p975": 0.001526444637827781, "res_p975": 0.0017444160695689382},
    "Psi_persistence_I":  {"raw": 0.022837296913806253,  "res": 0.023108397313261055,
                           "raw_p975": 0.017537515742347375, "res_p975": 0.01752236454678525},
}
SOLVED_OFFSETS = {0.10: 0.04977134874876729, 0.25: 0.12339551870278656, 0.50: 0.24248438819907564}
K_ONSET = 2          # Mike-arbitrated A2
S_ONSET = 3          # Mike-arbitrated A2
RHO_ORIGIN = 0.35
RHO_BAND = (0.35, 0.55)
N_GLOBAL_BINS = int(np.ceil((RHO_BAND[1] - RHO_BAND[0]) / DELTA_RHO))   # bins 0..N-1 cover [0.35, 0.55)
EPS_VAR = 1e-9       # committed Moran zero-variance guard; declared machine-scale epsilon
XCHK_ATOL = 1e-9     # recorded-vs-reconstructed tolerance (fixed; fail closed beyond it)
AXES = ["Psi_meanI_state", "Psi_persistence_I"]

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
# Byte-for-byte copies (committed c3_w2_tcop.py)
# ==========================================

def sanitize_float(v):
    return f"{v:+.4f}".replace("-", "m").replace("+", "p").replace(".", "_")

def u_t_for(mode, tier, u_const, block_idx):
    """Single source of truth for the common-mode input at a block."""
    if mode == "cm0":
        return u_const
    if tier == 0.0:
        return 0.0
    return [0.0, tier / 2.0, tier][block_idx % 3]

# ==========================================
# Helpers (threshold_fixing_read.py v3 conventions)
# ==========================================

def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))

def reconstruct_p_become(states_tick, kappa, u_level=0.0):
    """The field that would update t -> t+1. No draw; no advance."""
    q = get_neighbor_count(states_tick) / 8.0
    return sigmoid(LOGIT_L + u_level + kappa * (2.0 * q - 1.0))

def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def q_lower(vals, q):
    return float(np.percentile(np.asarray(vals, dtype=float), q, method=QUANTILE_METHOD))

def halt(reason, results=None):
    """Fail closed: record halt, emit nothing but the halt record, raise."""
    print(f"FAIL CLOSED: {reason}")
    if results is not None:
        results.setdefault("invalid_halt_record", []).append(reason)
        with open(OUT_JSON + ".HALT.json", "w") as f:
            json.dump(results, f, indent=1)
    raise RuntimeError(f"FAIL CLOSED: {reason}")

def npz_path(mode, kappa, tier, u_const, seed):
    kstr = sanitize_float(kappa)
    if mode == "cm1":
        return os.path.join(DATA, f"c3_w2_tcop_cm1_states_L0.4_k{kstr}_u{sanitize_float(tier)}_s{seed}.npz")
    return os.path.join(DATA, f"c3_w2_tcop_cm0_states_L0.4_k{kstr}_uc{sanitize_float(u_const)}_s{seed}.npz")

def rho_bin(wmr):
    """Global half-open bin on window_mean_rho; None if out of band."""
    if wmr < RHO_BAND[0] or wmr >= RHO_BAND[1]:
        return None
    return int((wmr - RHO_ORIGIN) / DELTA_RHO)

TEMPLATE = np.tile(np.array([0.0, 0.5, 1.0]) - 0.5, 4)   # centered, phase 0 = construction phase

def regress_on_template(block_means, phi):
    tmpl = np.roll(TEMPLATE, phi)
    cov = float(np.mean((block_means - block_means.mean()) * (tmpl - tmpl.mean())))
    var_t = float(np.var(tmpl))
    beta = cov / var_t
    denom = float(np.std(block_means) * np.std(tmpl))
    r = cov / denom if denom > 1e-15 else 0.0
    return r, beta, cov

def block_autocorr(block_means, lag):
    """Block-rho autocorrelation at integer lag over the primary block means (diagnostic)."""
    a, b = block_means[:-lag], block_means[lag:]
    sa, sb = float(np.std(a)), float(np.std(b))
    if sa < 1e-15 or sb < 1e-15:
        return 0.0
    return float(np.mean((a - a.mean()) * (b - b.mean())) / (sa * sb))

def verify_byte_for_byte(results):
    """C7: each copied function's source must appear VERBATIM in its committed origin."""
    pairs = [
        (COMMITTED_M2_SRC, [calculate_morans_i_toroidal_8, batch_morans_i_toroidal_8, get_neighbor_count]),
        (COMMITTED_TCOP_SRC, [u_t_for, sanitize_float]),
    ]
    record = {}
    for src_path, fns in pairs:
        if not os.path.exists(src_path):
            halt(f"committed source missing for byte-for-byte check: {src_path}", results)
        with open(src_path, "r", encoding="utf-8") as f:
            committed = f.read()
        for fn in fns:
            local_src = inspect.getsource(fn)
            if local_src not in committed:
                halt(f"byte-for-byte FAIL: {fn.__name__} source not verbatim in {src_path}", results)
            record[fn.__name__] = {"origin": src_path, "verbatim": True}
    results["byte_for_byte_enforcement"] = record

# ==========================================
# Main
# ==========================================

def main():
    if sys.prefix == sys.base_prefix:
        raise RuntimeError("PRE-FLIGHT FAIL: Virtual environment is not active.")

    results = {"read_constants": {
        "READ_RNG_SEED": READ_RNG_SEED,
        "READ_RNG_SEED_provenance": "SPEC-FIXED (TCOP_READ_SPEC.md Section 2); the threshold JSON's 20260704 is the threshold read's own seed and is never compared",
        "PERMUTATIONS": PERMUTATIONS,
        "quantile_method": QUANTILE_METHOD,
        "residue_definition": "abs(raw_stat - mean_control_stat)",
        "controls": {"Psi_meanI_state": "per-cell independent time-shuffle (argsort axis=0)",
                     "Psi_persistence_I": "spatial permutation of persistence grid (committed compute_persistence_null convention)"},
        "primary_blocks": PRIMARY_BLOCKS, "primary_window_starts_ticks": PRIMARY_WINDOW_STARTS,
        "onset_floors_operative_max_observed": ONSET,
        "k_onset": K_ONSET, "s_onset": S_ONSET,
        "rho_bin_grid": {"origin": RHO_ORIGIN, "width": DELTA_RHO, "band": list(RHO_BAND),
                         "n_global_bins": N_GLOBAL_BINS, "rule": "half-open [origin+k*w, origin+(k+1)*w); every global bin evaluated per pair/axis"},
        "eps_var_zero_variance": EPS_VAR, "crosscheck_atol": XCHK_ATOL,
        "iteration_order": "seed(READ_RNG_SEED) once; CM-0 sorted (tier,c_label,seed) then CM-1 sorted (tier,c_label,seed); per window: 199 meanI time-shuffles then 199 persistence spatial permutations",
        "cm0_first_discipline": "CM-1 NPZs are hashed for the input manifest at startup; no CM-1 NPZ is loaded (np.load) or statistically processed before the CM-0 comparator sets are computed and digest-frozen",
        "no_rerun_discipline": "This read may not be rerun with a different control seed to move any outcome.",
        "amendment_1": "Path-(a) failure bin-qualified per TCOP_READ_SPEC_AMENDMENT_1.md (Mike-arbitrated B1 option (i))",
        "disclosed_notes": ["N1 q05 gate method=lower (block-pooled operative convention) vs recorded default-method crosscheck",
                            "N2 c=0 zero-variance/non-identifiable, never numeric in trend",
                            "N3 recorded z travels recorded-not-reconstructed, never gates",
                            "N4 onset flags global; outcome bins gate-fenced; path-(a) bin-qualified (Amendment 1)",
                            "N5 verified lift = strict-all 5 seed rows pass G1",
                            "N6 fixed iteration order for RNG determinism",
                            "N7 empty-both-sides global bins reported as compact out-of-support index list"],
    }}

    # ---------- C7: byte-for-byte enforcement ----------
    verify_byte_for_byte(results)
    print("byte-for-byte enforcement PASS (5 functions verbatim in committed origins)")

    # ---------- Section 1: fail-closed manifest & structural verification ----------
    print("== Section 1: manifest & structural verification ==")
    for p in [BLOCK_CSV, WINDOW_CSV, PREFLIGHT_JSON, THRESH_JSON]:
        if not os.path.exists(p):
            halt(f"missing input {p}", results)
    with open(THRESH_JSON) as f:
        tj = json.load(f)
    checks = [
        (tj["g1_imprint"]["correlation_threshold"], G1_CORR, "G1 corr"),
        (tj["g1_imprint"]["slope_amplitude_threshold"], G1_SLOPE, "G1 slope"),
        (tj["g1_overdispersion"]["floor_overdispersion_threshold"], G1B_VAR, "G1b var"),
        (tj["g2_anchor"]["activation_floor_pos"], G2_FLOOR_POS, "G2 pos"),
        (tj["g2_anchor"]["activation_floor_neg"], G2_FLOOR_NEG, "G2 neg"),
        (tj["g3_rho_match"]["Delta_rho_match"], DELTA_RHO, "Delta_rho_match"),
        (tj["g4_compression"]["constants"]["mean_slope_floor_lower10"], G4_MEAN_FLOOR, "G4 mean"),
        (tj["g4_compression"]["constants"]["q05_slope_floor_lower10"], G4_Q05_FLOOR, "G4 q05"),
        (tj["g4_compression"]["constants"]["tail_mass_ceiling_max_observed"], G4_TAIL_CEIL, "G4 tail"),
        (tj["onset_null"]["Psi_meanI_state"]["raw_max"], ONSET["Psi_meanI_state"]["raw"], "onset meanI raw"),
        (tj["onset_null"]["Psi_meanI_state"]["residue_max"], ONSET["Psi_meanI_state"]["res"], "onset meanI res"),
        (tj["onset_null"]["Psi_persistence_I"]["raw_max"], ONSET["Psi_persistence_I"]["raw"], "onset pers raw"),
        (tj["onset_null"]["Psi_persistence_I"]["residue_max"], ONSET["Psi_persistence_I"]["res"], "onset pers res"),
        (tj["onset_null"]["Psi_meanI_state"]["raw_p97_5_method_lower"], ONSET["Psi_meanI_state"]["raw_p975"], "onset meanI raw p97.5"),
        (tj["onset_null"]["Psi_meanI_state"]["residue_p97_5_method_lower"], ONSET["Psi_meanI_state"]["res_p975"], "onset meanI res p97.5"),
        (tj["onset_null"]["Psi_persistence_I"]["raw_p97_5_method_lower"], ONSET["Psi_persistence_I"]["raw_p975"], "onset pers raw p97.5"),
        (tj["onset_null"]["Psi_persistence_I"]["residue_p97_5_method_lower"], ONSET["Psi_persistence_I"]["res_p975"], "onset pers res p97.5"),
    ]
    for got, want, name in checks:
        if float(got) != float(want):
            halt(f"threshold mismatch {name}: JSON {got} vs spec {want}", results)
    if int(tj["g3_bin_eligibility"]["N_bin_min"]) != N_BIN_MIN:
        halt("N_bin_min mismatch vs threshold JSON", results)
    if int(tj["g3_bin_eligibility"]["S_bin_min"]) != S_BIN_MIN:
        halt("S_bin_min mismatch vs threshold JSON", results)
    if int(tj["read_constants"]["PERMUTATIONS"]) != PERMUTATIONS:
        halt("PERMUTATIONS mismatch vs threshold JSON", results)
    if [float(x) for x in tj["g4_compression"]["constants"]["hard_interval"]] != [HARD_LO, HARD_HI]:
        halt("hard interval mismatch vs threshold JSON", results)

    with open(PREFLIGHT_JSON) as f:
        pj = json.load(f)
    if pj.get("script_sha256") != PREFLIGHT_SCRIPT_SHA:
        halt("preflight script digest mismatch vs lineage", results)
    for u in U_TIERS:
        if float(pj["static_offsets"][str(u)]["selected"]) != SOLVED_OFFSETS[u]:
            halt(f"solved offset mismatch tier {u}", results)

    bdf = pd.read_csv(BLOCK_CSV)
    wdf = pd.read_csv(WINDOW_CSV)
    if len(bdf) != 5040:
        halt(f"block rows {len(bdf)} != 5040", results)
    if len(wdf) != 4095:
        halt(f"window rows {len(wdf)} != 4095", results)

    # Expected run set + per-run row decomposition
    runs = []
    for (c, k) in KAPPA_MAP:
        for seed in SEEDS:
            runs.append({"mode": "cm1", "c_label": c, "kappa": k, "tier": 0.0, "u_const": None, "seed": seed})
    for (c, k) in KAPPA_MAP:
        for u in U_TIERS:
            for seed in SEEDS:
                runs.append({"mode": "cm1", "c_label": c, "kappa": k, "tier": u, "u_const": None, "seed": seed})
    for (c, k) in KAPPA_MAP:
        for u in U_TIERS:
            for seed in SEEDS:
                runs.append({"mode": "cm0", "c_label": c, "kappa": k, "tier": u, "u_const": SOLVED_OFFSETS[u], "seed": seed})
    for r in runs:
        r["npz"] = npz_path(r["mode"], r["kappa"], r["tier"], r["u_const"], r["seed"])
        r["run_id"] = os.path.basename(r["npz"])[:-4]
    n_cm1 = sum(1 for r in runs if r["mode"] == "cm1")
    n_cm0 = sum(1 for r in runs if r["mode"] == "cm0")
    if (n_cm1, n_cm0) != (180, 135):
        halt(f"run decomposition {n_cm1}/{n_cm0} != 180/135", results)
    manifest = {"npz": [], "csv": {os.path.basename(BLOCK_CSV): sha256_of(BLOCK_CSV),
                                   os.path.basename(WINDOW_CSV): sha256_of(WINDOW_CSV)},
                "preflight_json_sha256": sha256_of(PREFLIGHT_JSON),
                "threshold_json_sha256": sha256_of(THRESH_JSON)}
    b_by_run = dict(tuple(bdf.groupby("run_id")))
    w_by_run = dict(tuple(wdf.groupby("run_id")))
    for r in runs:
        if not os.path.exists(r["npz"]):
            halt(f"missing NPZ {r['npz']}", results)
        manifest["npz"].append({"file": os.path.basename(r["npz"]), "sha256": sha256_of(r["npz"])})
        rid = r["run_id"]
        if rid not in b_by_run or len(b_by_run[rid]) != N_BLOCKS:
            halt(f"block rows for {rid} missing or != 16", results)
        if rid not in w_by_run or len(w_by_run[rid]) != 13:
            halt(f"window rows for {rid} missing or != 13", results)
        # D2: exact index sets, no duplicates
        b_idx = sorted(int(x) for x in b_by_run[rid]["block_idx"])
        if b_idx != list(range(16)):
            halt(f"block_idx set for {rid} != 0..15 exactly once", results)
        w_st = sorted(int(x) for x in w_by_run[rid]["window_start_tick"])
        if w_st != ALL_WINDOW_STARTS:
            halt(f"window_start_tick set for {rid} != 0,25,...,300 exactly once", results)
        # D2: identifier columns vs manifest, every row
        for df in (b_by_run[rid], w_by_run[rid]):
            for _, row in df.iterrows():
                if str(row["mode"]) != r["mode"]:
                    halt(f"mode mismatch in CSV for {rid}", results)
                if float(row["c_label"]) != r["c_label"]:
                    halt(f"c_label mismatch in CSV for {rid}", results)
                if float(row["kappa"]) != r["kappa"]:
                    halt(f"kappa mismatch in CSV for {rid}", results)
                if float(row["tier"]) != r["tier"]:
                    halt(f"tier mismatch in CSV for {rid}", results)
                if int(row["seed"]) != r["seed"]:
                    halt(f"seed mismatch in CSV for {rid}", results)
                uc = row["u_const"]
                if r["mode"] == "cm0":
                    if pd.isna(uc) or abs(float(uc) - r["u_const"]) > XCHK_ATOL:
                        halt(f"u_const mismatch in CSV for {rid}", results)
                else:
                    if not (pd.isna(uc) or str(uc) == ""):
                        halt(f"u_const should be empty for cm1 row {rid}", results)
    try:
        manifest["read_script_sha256"] = sha256_of(os.path.abspath(__file__))
    except Exception:
        manifest["read_script_sha256"] = "unavailable"
    results["input_manifest"] = manifest
    print(f"  structural verification PASS: 315 runs, 5040/4095 rows, index sets exact, identifiers verified, all NPZs digested")

    # Fixed iteration orders (N6)
    cm0_runs = sorted([r for r in runs if r["mode"] == "cm0"], key=lambda r: (r["tier"], r["c_label"], r["seed"]))
    cm1_runs = sorted([r for r in runs if r["mode"] == "cm1"], key=lambda r: (r["tier"], r["c_label"], r["seed"]))

    np.random.seed(READ_RNG_SEED)
    xchk = {"checked": 0, "worst_abs_diff": 0.0, "columns": {}}
    def check(name, got, want, ctx):
        d = abs(float(got) - float(want))
        xchk["checked"] += 1
        xchk["worst_abs_diff"] = max(xchk["worst_abs_diff"], d)
        col = xchk["columns"].setdefault(name, {"n": 0, "worst": 0.0})
        col["n"] += 1
        col["worst"] = max(col["worst"], d)
        if d > XCHK_ATOL:
            halt(f"recorded-vs-reconstructed mismatch [{name}] {ctx}: recorded {want} vs reconstructed {got} (|d|={d})", results)

    invariance_checked = False
    sentinel_events = []

    def process_run(r, collect_comparator=None, gate_records=None):
        nonlocal invariance_checked
        rid = r["run_id"]
        st = np.load(r["npz"])["states"]
        if st.shape != (TICKS, GRID_SIZE, GRID_SIZE):
            halt(f"NPZ shape {st.shape} for {rid}", results)
        brows = b_by_run[rid].sort_values("block_idx")
        wrows = w_by_run[rid].sort_values("window_start_tick")
        rhos = st.reshape(TICKS, -1).mean(axis=1)

        # --- schedule ground truth + block_rho + flags (exhaustive) ---
        for _, br in brows.iterrows():
            b = int(br["block_idx"])
            u_expect = u_t_for(r["mode"], r["tier"], r["u_const"], b)
            check("u_t", u_expect, br["u_t"], f"{rid} b{b}")
            if int(br["schedule_phase"]) != b % 3:
                halt(f"schedule_phase mismatch {rid} b{b}", results)
            if bool(br["block_in_primary_set"]) != (3 <= b <= 14):
                halt(f"block_in_primary_set mismatch {rid} b{b}", results)
            check("block_rho", float(rhos[b*BLOCK:(b+1)*BLOCK].mean()), br["block_rho"], f"{rid} b{b}")

        block_means = np.array([rhos[b*BLOCK:(b+1)*BLOCK].mean() for b in PRIMARY_BLOCKS])

        rec = {"mode": r["mode"], "c_label": r["c_label"], "kappa": r["kappa"], "tier": r["tier"],
               "u_const": r["u_const"], "seed": r["seed"]}

        # --- regression statistics + D6 zero-mode diagnostics ---
        phase_stats = [regress_on_template(block_means, phi) for phi in range(3)]
        rec["regression_phase0_r_beta_cov"] = list(phase_stats[0])
        rec["regression_lag_diag_phases_1_2"] = [list(phase_stats[1]), list(phase_stats[2])]
        rec["block_rho_variance_ddof0"] = float(np.var(block_means))
        rec["g1b_above_floor_var"] = bool(rec["block_rho_variance_ddof0"] > G1B_VAR)
        rec["zero_mode_diagnostics"] = {
            "block_rho_variance_ddof0": rec["block_rho_variance_ddof0"],
            "schedule_regression_phase0_r_beta_cov": list(phase_stats[0]),
            "phase_1_2_diagnostics": [list(phase_stats[1]), list(phase_stats[2])],
            "block_rho_autocorr_lag_1_2_3": [block_autocorr(block_means, 1),
                                             block_autocorr(block_means, 2),
                                             block_autocorr(block_means, 3)],
            "note": "Diagnostic only; never a gate.",
        }

        if collect_comparator is not None:
            key = (r["c_label"], r["tier"])
            cset = collect_comparator.setdefault(key, {"r": [], "beta": [], "var": []})
            for phi in range(3):
                cset["r"].append(phase_stats[phi][0])
                cset["beta"].append(phase_stats[phi][1])
            cset["var"].append(rec["block_rho_variance_ddof0"])

        # --- G4 + G2 reconstruction over primary blocks (gate source) ---
        g4_blocks = {"mean_slope": [], "q05_lower": [], "q05_default_xchk": [], "tail_mass": [],
                     "p_min": [], "p_max": [], "mean_p": []}
        propI_blocks, propI_masked_blocks = [], []
        for b in PRIMARY_BLOCKS:
            b_states = st[b*BLOCK:(b+1)*BLOCK]
            u_lvl = u_t_for(r["mode"], r["tier"], r["u_const"], b)
            pb = np.stack([reconstruct_p_become(b_states[i], r["kappa"], u_lvl) for i in range(BLOCK)])
            sl = pb * (1.0 - pb)
            g4_blocks["mean_slope"].append(float(sl.mean()))
            g4_blocks["q05_lower"].append(q_lower(sl.ravel(), 5))
            g4_blocks["q05_default_xchk"].append(float(np.percentile(sl, 5)))
            g4_blocks["tail_mass"].append(float(np.mean((pb < HARD_LO) | (pb > HARD_HI))))
            g4_blocks["p_min"].append(float(pb.min()))
            g4_blocks["p_max"].append(float(pb.max()))
            g4_blocks["mean_p"].append(float(pb.mean()))
            # prop_I per block: zero-variance handling BEFORE any Moran call (N2)
            tick_Is, tick_Is_m = [], []
            zv = 0
            for i in range(BLOCK):
                if float(np.var(pb[i])) < EPS_VAR:
                    zv += 1
                    tick_Is.append(None)
                    tick_Is_m.append(None)
                else:
                    tick_Is.append(calculate_morans_i_toroidal_8(pb[i]))
                    inact = (b_states[i] == 0)
                    if inact.any() and (~inact).any():
                        pm = pb[i].copy(); pm[~inact] = pb[i][inact].mean()
                        tick_Is_m.append(calculate_morans_i_toroidal_8(pm))
                    else:
                        tick_Is_m.append(0.0)
            br = brows[brows["block_idx"] == b].iloc[0]
            if zv == BLOCK:
                propI_blocks.append(None)   # zero-variance / non-identifiable
                propI_masked_blocks.append(None)
                if abs(float(br["prop_I_full_surface"])) > 1e-15:
                    halt(f"recorded prop_I nonzero at zero-variance block {rid} b{b}", results)
                if abs(float(br["prop_I_masked_diagnostic"])) > 1e-15:
                    halt(f"recorded masked prop_I nonzero at zero-variance block {rid} b{b}", results)
            elif zv == 0:
                propI_blocks.append(float(np.mean(tick_Is)))
                propI_masked_blocks.append(float(np.mean(tick_Is_m)))
                check("prop_I_full_surface", propI_blocks[-1], br["prop_I_full_surface"], f"{rid} b{b}")
                check("prop_I_masked_diagnostic", propI_masked_blocks[-1], br["prop_I_masked_diagnostic"], f"{rid} b{b}")
            else:
                halt(f"mixed zero-variance ticks within block {rid} b{b} ({zv}/{BLOCK}) — route to Mike", results)
            # cross-check recorded block G4 columns (like-for-like)
            check("mean_slope", g4_blocks["mean_slope"][-1], br["mean_slope"], f"{rid} b{b}")
            check("q05_slope_recorded_default", g4_blocks["q05_default_xchk"][-1], br["q05_slope"], f"{rid} b{b}")
            check("tail_mass", g4_blocks["tail_mass"][-1], br["tail_mass"], f"{rid} b{b}")
            check("p_min", g4_blocks["p_min"][-1], br["p_min"], f"{rid} b{b}")
            check("p_max", g4_blocks["p_max"][-1], br["p_max"], f"{rid} b{b}")
            check("mean_p_become", g4_blocks["mean_p"][-1], br["mean_p_become"], f"{rid} b{b}")
            check("raw_block_Psi_meanI", float(np.mean(batch_morans_i_toroidal_8(b_states))),
                  br["raw_Psi_meanI_state"], f"{rid} b{b}")
            check("raw_block_Psi_pers", float(calculate_morans_i_toroidal_8(np.mean(b_states, axis=0))),
                  br["raw_Psi_persistence_I"], f"{rid} b{b}")

        rec["g4"] = {
            "min_mean_slope": float(min(g4_blocks["mean_slope"])),
            "min_q05_slope_method_lower": float(min(g4_blocks["q05_lower"])),
            "max_tail_mass": float(max(g4_blocks["tail_mass"])),
            "p_min": float(min(g4_blocks["p_min"])), "p_max": float(max(g4_blocks["p_max"])),
            "margins": {"mean_slope": float(min(g4_blocks["mean_slope"]) - G4_MEAN_FLOOR),
                        "q05_slope": float(min(g4_blocks["q05_lower"]) - G4_Q05_FLOOR),
                        "tail_mass": float(G4_TAIL_CEIL - max(g4_blocks["tail_mass"]))},
            "convention_note": "q05 gate is block-pooled method='lower' (operative code convention; not identical to a per-tick min-q05 rule).",
        }
        rec["g4_pass"] = bool(rec["g4"]["min_mean_slope"] >= G4_MEAN_FLOOR and
                              rec["g4"]["min_q05_slope_method_lower"] >= G4_Q05_FLOOR and
                              rec["g4"]["max_tail_mass"] <= G4_TAIL_CEIL)
        if all(v is None for v in propI_blocks):
            rec["prop_I_row"] = None
            rec["prop_I_status"] = "zero-variance / non-identifiable, consistent with spatially constant"
        else:
            rec["prop_I_row"] = float(np.mean([v for v in propI_blocks if v is not None]))
            rec["prop_I_status"] = "numeric"
            rec["prop_I_masked_diag_row"] = float(np.mean([v for v in propI_masked_blocks if v is not None]))

        rec["g1_applicable"] = bool(r["mode"] == "cm1" and r["tier"] > 0.0)

        # --- windows: mean rho, raw Psi (gate source), residues, onset ---
        run_onset = {ax: [] for ax in AXES}
        for _, wr in wrows.iterrows():
            ws = int(wr["window_start_tick"])
            wsb = ws // BLOCK
            in_primary = (3 <= wsb <= 11)
            if bool(wr["window_in_primary_family"]) != in_primary:
                halt(f"window_in_primary_family mismatch {rid} w{ws}", results)
            wmr = float(rhos[ws:ws+WINDOW_LEN].mean())
            check("window_mean_rho", wmr, wr["window_mean_rho"], f"{rid} w{ws}")
            if not in_primary:
                continue
            win = st[ws:ws+WINDOW_LEN]
            tick_Is = batch_morans_i_toroidal_8(win)
            raw_mI = float(np.mean(tick_Is))
            pgrid = np.mean(win, axis=0)
            raw_pI = float(calculate_morans_i_toroidal_8(pgrid))
            check("raw_Psi_meanI_state", raw_mI, wr["raw_Psi_meanI_state"], f"{rid} w{ws}")
            check("raw_Psi_persistence_I", raw_pI, wr["raw_Psi_persistence_I"], f"{rid} w{ws}")
            # meanI control: per-cell independent time shuffle (axis=0), 199 perms
            flat = win.reshape(WINDOW_LEN, -1)
            null_mI = np.zeros(PERMUTATIONS)
            for p in range(PERMUTATIONS):
                rand_idx = np.random.rand(WINDOW_LEN, N_CELLS).argsort(axis=0)
                shuffled = np.take_along_axis(flat, rand_idx, axis=0).reshape(WINDOW_LEN, GRID_SIZE, GRID_SIZE)
                null_mI[p] = np.mean(batch_morans_i_toroidal_8(shuffled))
                if not invariance_checked:
                    if not bool(np.allclose(np.mean(shuffled, axis=0), pgrid)):
                        halt("invariance self-check FAILED: time shuffle did not preserve persistence grid", results)
                    results["read_constants"]["invariance_selfcheck"] = True
                    invariance_checked = True
            res_mI = abs(raw_mI - float(np.mean(null_mI)))
            # persistence control: spatial permutation, 199 perms
            flat_p = pgrid.flatten()
            null_pI = np.zeros(PERMUTATIONS)
            for p in range(PERMUTATIONS):
                shuf = np.random.permutation(flat_p).reshape((GRID_SIZE, GRID_SIZE))
                null_pI[p] = calculate_morans_i_toroidal_8(shuf)
            res_pI = abs(raw_pI - float(np.mean(null_pI)))
            for ax, raw_v, res_v, zcol in [("Psi_meanI_state", raw_mI, res_mI, "Psi_meanI_state_z"),
                                           ("Psi_persistence_I", raw_pI, res_pI, "Psi_persistence_I_z")]:
                exceed = bool(abs(raw_v) > ONSET[ax]["raw"] and res_v > ONSET[ax]["res"])
                wrec = {"window_start_tick": ws, "phase": wsb % 3, "bin": rho_bin(wmr), "wmr": wmr,
                        "raw_signed": raw_v, "raw_abs": abs(raw_v), "residue": res_v,
                        "z_recorded_not_reconstructed": float(wr[zcol]), "exceeds": exceed}
                run_onset[ax].append(wrec)
                if exceed:
                    sentinel_events.append({"axis": ax, "run_id": rid, **{k: rec[k] for k in
                                            ("mode", "c_label", "tier", "seed")}, **wrec})
        for ax in AXES:
            n_ex = sum(1 for w in run_onset[ax] if w["exceeds"])
            rec.setdefault("onset", {})[ax] = {
                "windows": run_onset[ax], "exceed_count": n_ex,
                "row_onset_flag": bool(n_ex >= K_ONSET),
                "exceed_phases": [w["phase"] for w in run_onset[ax] if w["exceeds"]],
            }
        if gate_records is not None:
            gate_records[rid] = rec
        return rec

    # ---------- Section 3.1 execution order: CM-0 pass FIRST ----------
    print("== CM-0 pass (comparator sets frozen before any CM-1 NPZ is loaded/processed) ==")
    comparators = {}
    cm0_records = {}
    for i, r in enumerate(cm0_runs):
        process_run(r, collect_comparator=comparators, gate_records=cm0_records)
        if (i + 1) % 15 == 0:
            print(f"  cm0 {i+1}/{len(cm0_runs)}")
    comp_out = {}
    for (c, tier), cset in comparators.items():
        if len(cset["r"]) != 15 or len(cset["var"]) != 5:
            halt(f"comparator set malformed for c={c}, tier={tier}", results)
        comp_out[f"c={c:+.2f},tier={tier:.2f}"] = {
            "r_15_signed": cset["r"], "beta_15_signed": cset["beta"], "var_5": cset["var"],
            "dominance_r": max(0.0, max(cset["r"])),
            "dominance_beta": max(0.0, max(cset["beta"])),
            "dominance_var": max(cset["var"]),
        }
    comp_digest = hashlib.sha256(json.dumps(comp_out, sort_keys=True).encode()).hexdigest()
    results["cm0_comparator_sets"] = {"sets": comp_out, "frozen_digest": comp_digest,
        "apparatus_limit": "15-point coarse comparator (5 seeds x 3 phases); conservative maxima, not a precision claim.",
        "rule": "Section 3.1: max(0, max signed r), max(0, max signed beta), max var; strict exceedance on all three."}
    results["cm0_row_records"] = cm0_records
    print(f"  comparator sets FROZEN, digest {comp_digest[:16]}...")

    # ---------- CM-1 pass ----------
    print("== CM-1 pass ==")
    cm1_records = {}
    for i, r in enumerate(cm1_runs):
        rec = process_run(r, gate_records=cm1_records)
        if rec["g1_applicable"]:
            key = f"c={r['c_label']:+.2f},tier={r['tier']:.2f}"
            dom = comp_out[key]
            r0, b0, _ = rec["regression_phase0_r_beta_cov"]
            rec["g1"] = {
                "slope_positive": bool(b0 > 0),
                "corr_above_floor": bool(r0 > G1_CORR),
                "slope_above_floor": bool(b0 > G1_SLOPE),
                "dominance": {"r": bool(r0 > dom["dominance_r"]),
                              "beta": bool(b0 > dom["dominance_beta"]),
                              "var": bool(rec["block_rho_variance_ddof0"] > dom["dominance_var"])},
                "margins": {"corr": float(r0 - G1_CORR), "slope": float(b0 - G1_SLOPE),
                            "dom_r": float(r0 - dom["dominance_r"]),
                            "dom_beta": float(b0 - dom["dominance_beta"]),
                            "dom_var": float(rec["block_rho_variance_ddof0"] - dom["dominance_var"])},
            }
            g1 = rec["g1"]
            rec["g1_pass"] = bool(g1["slope_positive"] and g1["corr_above_floor"] and g1["slope_above_floor"]
                                  and all(g1["dominance"].values()))
        else:
            rec["g1_pass"] = None   # u=0 tier: G1-exempt by contract
        if (i + 1) % 15 == 0:
            print(f"  cm1 {i+1}/{len(cm1_runs)}")
    results["cm1_row_records"] = cm1_records
    results["consistency_audit"] = xchk

    # ---------- G2 tier/sign aggregation ----------
    print("== G2 aggregation ==")
    g2_out = {}
    for tier in U_TIERS:
        for sign, floor in [("pos", G2_FLOOR_POS), ("neg", G2_FLOOR_NEG)]:
            sgn = 1 if sign == "pos" else -1
            seq = {}
            for mag in [0.05, 0.10, 0.20, 0.35]:
                c = sgn * mag
                vals = [cm1_records[r["run_id"]]["prop_I_row"] for r in cm1_runs
                        if r["tier"] == tier and r["c_label"] == c]
                seq[f"{mag:.2f}"] = {"per_seed_row_means": vals, "median": float(np.median(vals)),
                                     "lower_support": q_lower(vals, 10)}
            med = [seq[f"{m:.2f}"]["median"] for m in [0.05, 0.10, 0.20, 0.35]]
            low = [seq[f"{m:.2f}"]["lower_support"] for m in [0.05, 0.10, 0.20, 0.35]]
            trend_med = bool(all(med[i+1] >= med[i] for i in range(3)))
            trend_low = bool(all(low[i+1] >= low[i] for i in range(3)))
            endpoint = bool(seq["0.35"]["lower_support"] >= floor)
            vals_by_mag = [seq[f"{m:.2f}"]["per_seed_row_means"] for m in [0.05, 0.10, 0.20, 0.35]]
            nonmono = sum(1 for s in range(5) for i in range(3) if vals_by_mag[i+1][s] < vals_by_mag[i][s])
            g2_out[f"tier={tier:.2f},{sign}"] = {
                "sequence": seq, "trend_median_nondecreasing": trend_med,
                "trend_lower_support_nondecreasing": trend_low,
                "endpoint_0.35_lower_support": seq["0.35"]["lower_support"],
                "endpoint_floor": floor, "endpoint_pass": endpoint,
                "per_seed_nonmonotone_steps_diag": nonmono,
                "g2_pass": bool(trend_med and trend_low and endpoint),
                "c0_status": "zero-variance / non-identifiable, consistent with spatially constant (never numeric in trend)",
            }
    results["g2_tier_sign"] = g2_out

    # ---------- Setting-level onset flags ----------
    settings = {}
    for r in cm1_runs:
        settings.setdefault((r["tier"], r["c_label"]), []).append(r["run_id"])
    setting_onset = {}
    for (tier, c), rids in settings.items():
        for ax in AXES:
            flags = [cm1_records[rid]["onset"][ax]["row_onset_flag"] for rid in rids]
            counts = [cm1_records[rid]["onset"][ax]["exceed_count"] for rid in rids]
            setting_onset[f"tier={tier:.2f},c={c:+.2f},{ax}"] = {
                "row_flags": flags, "row_exceed_counts": counts,
                "seeds_with_flag": int(sum(flags)),
                "setting_onset_flag": bool(sum(flags) >= S_ONSET),
            }
    results["setting_onset"] = setting_onset
    results["sentinel_events"] = sentinel_events

    # ---------- Verified common-mode lift (N5) ----------
    lift = {}
    for tier in U_TIERS:
        rids = settings[(tier, 0.0)]
        passes = [bool(cm1_records[rid]["g1_pass"]) for rid in rids]
        lift[f"tier={tier:.2f}"] = {"c0_row_g1_passes": passes, "verified_lift_all5": bool(all(passes))}
    results["verified_lift_c0"] = lift

    # ---------- G3 binning + comparison universe + outcome ----------
    print("== G3 + outcome evaluation ==")
    def setting_windows(tier, c, ax):
        """Primary windows of a setting eligible for OUTCOME bins (N4 gate fencing)."""
        out = []
        for rid in settings[(tier, c)]:
            rec = cm1_records[rid]
            if not rec["g4_pass"]:
                continue
            if rec["g1_applicable"] and not rec["g1_pass"]:
                continue
            for w in rec["onset"][ax]["windows"]:
                if w["bin"] is not None:
                    out.append({"seed": rec["seed"], **w})
        return out

    def bin_side(wins, b):
        return [w for w in wins if w["bin"] == b]

    def eligibility(side1, side2):
        n1, n2 = len(side1), len(side2)
        if n1 < N_BIN_MIN or n2 < N_BIN_MIN:
            return "count-failed"
        for side in (side1, side2):
            sc = {}
            for w in side:
                sc[w["seed"]] = sc.get(w["seed"], 0) + 1
            if len(sc) < S_BIN_MIN:
                return "seed-failed"
            if max(sc.values()) > len(side) / 2.0:
                return "seed-failed"
        h1 = [sum(1 for w in side1 if w["phase"] == p) for p in range(3)]
        h2 = [sum(1 for w in side2 if w["phase"] == p) for p in range(3)]
        if any(abs(h1[p] - h2[p]) > 1 for p in range(3)):
            return "phase-confounded"
        return "eligible"

    # comparison universe (spec 4.3; D2 of the spec merge)
    universe = []
    tiers_all = [0.0] + U_TIERS
    for i in range(len(tiers_all)):
        for j in range(i+1, len(tiers_all)):
            universe.append({"path": "a", "side1": (tiers_all[i], 0.0), "side2": (tiers_all[j], 0.0)})
    mags = [0.0, 0.05, 0.10, 0.20, 0.35]
    for tier in U_TIERS:
        for sign in (+1, -1):
            for i in range(len(mags)):
                for j in range(i+1, len(mags)):
                    universe.append({"path": "b", "sign": sign, "tier": tier,
                                     "side1": (tier, sign*mags[i] if mags[i] > 0 else 0.0),
                                     "side2": (tier, sign*mags[j])})
    seen, uni = set(), []
    for u in universe:
        key = (u["path"], u.get("sign"), u["side1"], u["side2"])
        if key not in seen:
            seen.add(key); uni.append(u)
    universe = uni

    g3_out = []
    tracking = {ax: [] for ax in AXES}
    # Amendment 1 evidence collectors
    path_a_binqual = {}          # (tier, ax) -> list of {pair, bin, exceeds_in_bin}
    elig_bins_a = {}             # (tier, ax) -> set of eligible path-(a) bins containing that side
    for pair in universe:
        for ax in AXES:
            w1 = setting_windows(*pair["side1"], ax)
            w2 = setting_windows(*pair["side2"], ax)
            pair_rec = {"path": pair["path"], "sign": pair.get("sign"),
                        "side1": list(pair["side1"]), "side2": list(pair["side2"]),
                        "axis": ax, "bins": {}, "bins_empty_out_of_support": []}
            for b in range(N_GLOBAL_BINS):    # D1: every global bin evaluated
                s1, s2 = bin_side(w1, b), bin_side(w2, b)
                if not s1 and not s2:
                    pair_rec["bins_empty_out_of_support"].append(b)   # N7 compaction
                    continue
                status = eligibility(s1, s2) if (s1 and s2) else "out-of-support"
                brec = {"status": status, "n1": len(s1), "n2": len(s2)}
                if status == "eligible":
                    ex1 = sum(1 for w in s1 if w["exceeds"]); ex2 = sum(1 for w in s2 if w["exceeds"])
                    re1 = float(np.mean([w["residue"] - ONSET[ax]["res"] for w in s1]))
                    re2 = float(np.mean([w["residue"] - ONSET[ax]["res"] for w in s2]))
                    brec.update({"exceed_1": ex1, "exceed_2": ex2,
                                 "mean_residue_excess_1": re1, "mean_residue_excess_2": re2,
                                 "mean_raw_abs_1": float(np.mean([w["raw_abs"] for w in s1])),
                                 "mean_raw_abs_2": float(np.mean([w["raw_abs"] for w in s2]))})
                    brec["burden_side2_lexicographic"] = bool(ex2 >= ex1 and (ex2 > ex1 or re2 > re1))
                    if pair["path"] == "a":   # Amendment 1 collectors
                        for side, exN in [(pair["side1"], ex1), (pair["side2"], ex2)]:
                            t_side = side[0]
                            elig_bins_a.setdefault((t_side, ax), set()).add(b)
                            if exN >= 1:
                                path_a_binqual.setdefault((t_side, ax), []).append(
                                    {"pair": [list(pair["side1"]), list(pair["side2"])], "bin": b, "exceeds_in_bin": exN})
                pair_rec["bins"][str(b)] = brec
            g3_out.append(pair_rec)
            if pair["path"] == "b" and pair["side1"][1] == 0.0 and abs(pair["side2"][1]) >= 0.20:
                tier = pair["tier"]; c2 = pair["side2"][1]
                flag2 = setting_onset[f"tier={tier:.2f},c={c2:+.2f},{ax}"]["setting_onset_flag"]
                flag0 = setting_onset[f"tier={tier:.2f},c={0.0:+.2f},{ax}"]["setting_onset_flag"]
                elig_burden = [b for b, br in pair_rec["bins"].items()
                               if br["status"] == "eligible" and br.get("burden_side2_lexicographic")]
                elig_any = [b for b, br in pair_rec["bins"].items() if br["status"] == "eligible"]
                sign_key = "pos" if c2 > 0 else "neg"
                g2p = g2_out[f"tier={tier:.2f},{sign_key}"]["g2_pass"]
                tracking[ax].append({
                    "tier": tier, "c_responsive": c2, "g2_pass_signtier": g2p,
                    "responsive_setting_flag": flag2, "c0_setting_flag": flag0,
                    "eligible_bins": elig_any, "eligible_bins_with_burden": elig_burden,
                    "tracks": bool(g2p and flag2 and (not flag0) and len(elig_burden) >= 1),
                })
    results["g3_pairs_bins"] = g3_out
    results["differential_tracking"] = tracking
    results["path_a_bin_qualification"] = {f"tier={t:.2f},{ax}": v for (t, ax), v in path_a_binqual.items()}

    # ---------- Outcome record (Section 7 + Amendment 1; candidate language) ----------
    outcome = {}
    for ax in AXES:
        # Amendment 1: path-(a) failure = global flag AND verified lift AND bin-qualified evidence
        path_a_fail = []
        for tier in U_TIERS:
            so = setting_onset[f"tier={tier:.2f},c={0.0:+.2f},{ax}"]
            vl = lift[f"tier={tier:.2f}"]["verified_lift_all5"]
            bq = path_a_binqual.get((tier, ax), [])
            if so["setting_onset_flag"] and vl and len(bq) >= 1:
                path_a_fail.append({"tier": tier, "setting_evidence": so, "bin_qualification": bq})
            elif so["setting_onset_flag"] and vl and len(bq) == 0:
                outcome.setdefault("_amendment1_withheld", []).append({
                    "axis": ax, "tier": tier,
                    "note": ("global setting flag + verified lift present but NO G3-eligible path-(a) bin "
                             "carries the onset evidence — NOT a path-(a) failure per Amendment 1; "
                             "recorded as apparatus-limited"),
                    "setting_evidence": so})
        # sentinel c=0 risky events, G3_eligible-tagged (Amendment 1)
        sent_risky = []
        for ev in sentinel_events:
            if ev["axis"] != ax or ev["mode"] != "cm1" or ev["c_label"] != 0.0 or ev["tier"] == 0.0:
                continue
            rec = cm1_records[ev["run_id"]]
            if rec["g1_pass"] and rec["g4_pass"] and ev["bin"] is not None:
                tagged = dict(ev)
                tagged["G3_eligible"] = bool(ev["bin"] in elig_bins_a.get((ev["tier"], ax), set()))
                sent_risky.append(tagged)
        tracks_any = [t for t in tracking[ax] if t["tracks"]]
        b_families_evaluable = [t for t in tracking[ax] if t["g2_pass_signtier"] and len(t["eligible_bins"]) >= 1]
        path_b_fail = bool(len(b_families_evaluable) >= 1 and len(tracks_any) == 0)
        produces = bool(len(tracks_any) >= 1 and len(path_a_fail) == 0)
        fails_a = bool(len(path_a_fail) >= 1)
        if produces:
            label = "PRODUCES the predicted ordering structure on this axis"
        elif fails_a and path_b_fail:
            label = "FAILS TO PRODUCE (risky form) on this axis: paths (a) and (b)"
        elif fails_a:
            label = "FAILS TO PRODUCE (risky form) on this axis: path (a) — organization under common-mode lift at kappa~0"
        elif path_b_fail:
            label = "FAILS TO PRODUCE (risky form) on this axis: path (b) — fails to produce differential tracking"
        elif len(b_families_evaluable) == 0 and len(path_a_fail) == 0:
            label = "UNDER-DETERMINED on this axis: no evaluable eligible comparison family (apparatus limits, not evidence)"
        else:
            label = "UNDER-DETERMINED on this axis"
        outcome[ax] = {
            "label": label,
            "evidence": {
                "tracking_families": tracking[ax],
                "families_tracking": tracks_any,
                "path_a_setting_failures_bin_qualified": path_a_fail,
                "sentinel_risky_events_c0_G3_tagged": sent_risky,
                "path_b_evaluable_families": len(b_families_evaluable),
                "verified_lift": lift,
            },
            "alternatives_excluded_note": (
                "G1 passes carry amplitude+correlation+three-component CM-0 dominance (correlation-only, "
                "floor-only, and overdispersion-only alternatives excluded); onset requires raw AND axis-appropriate "
                "residue (raw-only and z-only alternatives excluded); path-(a) failure requires bin-qualified evidence "
                "(gate-failed/out-of-support/phase-confounded alternatives excluded per Amendment 1); tracking requires "
                "setting flags AND in-bin lexicographic burden inside G3-eligible phase-matched bins (un-stratified "
                "sweep excluded)."),
            "qualified_wording": ("Any schedule-following rho_t structure is 'zero-mode driver imprint' — "
                                  "apparatus-level only; not coherence, not Regime II; unqualified 'synchrony' excluded; "
                                  "lift without organization = lift without SPATIAL/DIFFERENTIAL organization."),
        }
    outcome["welding_subreading_note"] = ("If differential prop_I rises (G2) but realized organization does not track, "
                                          "the welding claim weakens — recorded as bearing on Reading B's realized-level "
                                          "content, distinct from the ordering claim. Grounds in g2_tier_sign + differential_tracking.")
    outcome["fences"] = ("No outcome reclassifies Comparator 0, moves L4, closes Rule E B/C, closes the CM-2 hold, "
                         "or closes any mechanism class. No density-stability claim.")
    results["outcome_classification"] = outcome
    results["invalid_halt_record"] = []

    with open(OUT_JSON, "w") as f:
        json.dump(results, f, indent=1)
    print(f"WROTE {OUT_JSON}")

    # ---------- Console summary (D5: counts only; the JSON evidence table governs) ----------
    print("== SUMMARY (counts only; outcome labels written to JSON; see evidence table) ==")
    print(f"consistency audit: {xchk['checked']} checks, worst |d| = {xchk['worst_abs_diff']:.3e} (atol {XCHK_ATOL})")
    for tier in U_TIERS:
        n_g1 = sum(1 for r in cm1_runs if r["tier"] == tier and cm1_records[r["run_id"]]["g1_pass"])
        print(f"G1 tier {tier}: {n_g1}/45 nonzero-tier rows pass (incl. dominance)")
    n_g4 = sum(1 for rid, rec in cm1_records.items() if rec["g4_pass"])
    print(f"G4: {n_g4}/180 CM-1 rows in-band")
    n_g2 = sum(1 for v in g2_out.values() if v["g2_pass"])
    print(f"G2: {n_g2}/6 tier-sign families pass")
    print(f"sentinel events: {len(sentinel_events)} total")
    n_set = sum(1 for v in setting_onset.values() if v["setting_onset_flag"])
    print(f"setting-level onset flags: {n_set} of {len(setting_onset)} setting-axis pairs")
    for ax in AXES:
        print(f"[{ax}] outcome label written to JSON; see evidence table")

if __name__ == "__main__":
    main()
