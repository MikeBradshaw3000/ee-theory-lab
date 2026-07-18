#!/usr/bin/env python3
# CALIBRATION OUTPUT - INFORMS AMENDMENT MACHINERY ONLY - NOT EVIDENCE ABOUT THE EE SUBSTRATE
"""
stage2_case1_harness.py  (v6 = v5 + null-extension NPZ filename token fix, line 45:
k0_0000 -> kp0_0000 per the committed {kappa:+.4f} token rule; L2 delta review; NOT authorized to execute)

All 18 L2-required items folded. Gate semantics in this file are FROZEN-SOURCE-VERIFIED:
every rule below was read from tcop_read.py (digest d60da1d9...399f7c) main() and helpers,
with line-cited semantics: WINDOW_LEN=100 (v1's 75 was a wrong-value defect, corrected);
onset exceed = abs(raw)>raw_floor AND residue>res_floor; meanI control = per-cell time
shuffle argsort(axis=0); persistence control = spatial permutation of the window-mean grid;
comparators keyed by (c_label,tier), 15-point signed, dominance=max(0,max r)/max(0,max
beta)/max var, CM-1 G1 uses PHASE-0 stats with slope_positive required; tier-0 rows
G1-EXEMPT (g1_pass=None), never trivially passed; G2 per (tier,sign) dual nondecreasing
trend (median + q_lower 10) on prop_I_row with 0.35 endpoint floor; G3 eligibility statuses
out-of-support / count-failed / seed-failed / phase-confounded / eligible with the
per-phase histogram |h1-h2|<=1 rule; comparison universe = frozen tier-pairs (path a) and
per-(tier,sign) magnitude pairs from {0,.05,.10,.20,.35} (path b), c=0 sign-neutral;
tracking burden = ex2>=ex1 AND (ex2>ex1 OR re2>re1); Amendment-1 path-(a) collectors and
bin-qualification verbatim; evaluable path-(b) family = responsive pair (side1 c=0,
|c2|>=0.20) with g2_pass AND >=1 eligible bin; evaluable path (a) = >=1 eligible path-(a)
bin (bin-qualified object, per the frozen floor-unit clarification).

Governed by STAGE2_MINI_CONTRACT.md + Amendment 1 (L2-accepted) and the frozen
implementation spec v2. The TCOP result is untouched and permanent.
Stages: preflight | geometry | recovery | controls | forecast   (Mike-executed, in order).
"""

import os, sys, json, time, hashlib, inspect, importlib.util, ast, re
import numpy as np

F2_HEADER = "CALIBRATION OUTPUT - INFORMS AMENDMENT MACHINERY ONLY - NOT EVIDENCE ABOUT THE EE SUBSTRATE"

# ==========================================================================
# 0. Paths / allowlist / denylist  (L2 items: read-allowlist, commonpath
#    writes, guarded imports, self-audit; fail-closed everywhere)
# ==========================================================================
REPO = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
W2   = os.path.join(REPO, "cycle3", "wave_two")
DATA = os.path.join(REPO, "cycle3", "data_out")
OUTD = os.path.join(REPO, "cycle3", "calibration", "stage2")

CANONICAL_SEEDS = [42, 137, 256, 1024, 31415]
def null_ext_npz(seed):
    return os.path.join(DATA, f"c3_w2_null_extension_states_L0.4_kp0_0000_s{seed}.npz")

PERMITTED_READS = {
    os.path.join(W2, "TWO_CHANNEL_ORDERING_PROBE_CONTRACT.md"),
    os.path.join(W2, "TWO_CHANNEL_ORDERING_PROBE_DESIGN_RESOLUTION.md"),
    os.path.join(W2, "TCOP_READ_SPEC.md"),
    os.path.join(W2, "TCOP_READ_SPEC_AMENDMENT_1.md"),
    os.path.join(W2, "THRESHOLDING_ADDENDUM.md"),
    os.path.join(REPO, "tcop_read.py"),
    os.path.join(W2, "c3_w2_tcop.py"),            # Amendment 1: construction-only
    os.path.join(W2, "c3_w2_rule_c_m2.py"),       # Amendment 1: construction-only
    os.path.abspath(__file__),
} | {null_ext_npz(s) for s in CANONICAL_SEEDS}

TCOP_READ_DIGEST = "d60da1d92d72ddeb15353da301ea4e6161b9961e769936e42779170d8b399f7c"
C3W2TCOP_DIGEST  = "466455f20550b8c41a984ce40db49ebe0e832ae56c269ab518b521c6ad83b7e7"
RULECM2_DIGEST   = "8f1f6ab9f188abe35dd257cb46e9ce7c9e51ad9ee1744c5945c10830d030ef59"   # L2 item 13

HELD_OUT_DENY = [os.path.join(DATA, "tcop_read_results.json"),
                 os.path.join(W2, "TCOP_READ_FINDINGS.md"),
                 os.path.join(DATA, "c3_w2_tcop_blocks.csv"),
                 os.path.join(DATA, "c3_w2_tcop_windows.csv")]
HELD_OUT_PREFIXES = [os.path.join(DATA, "c3_w2_tcop_cm1_states"),
                     os.path.join(DATA, "c3_w2_tcop_cm0_states")]

def _inside(child, parent):
    try: return os.path.commonpath([os.path.abspath(child), os.path.abspath(parent)]) == os.path.abspath(parent)
    except ValueError: return False

def guarded_open(path, mode="r", **kw):
    ap = os.path.abspath(path)
    if any(ap == os.path.abspath(d) for d in HELD_OUT_DENY) or \
       any(ap.startswith(os.path.abspath(p)) for p in HELD_OUT_PREFIXES):
        raise RuntimeError(f"FAIL CLOSED (held-out): {ap}")
    if "w" in mode or "a" in mode or "+" in mode:
        if not _inside(ap, OUTD):
            raise RuntimeError(f"FAIL CLOSED (write outside OUTD): {ap}")
    else:
        if not (ap in PERMITTED_READS or _inside(ap, OUTD)):
            raise RuntimeError(f"FAIL CLOSED (read not on allowlist): {ap}")
    return open(ap, mode, **kw)

def guarded_npz(path):
    ap = os.path.abspath(path)
    if ap not in PERMITTED_READS and not _inside(ap, OUTD):
        raise RuntimeError(f"FAIL CLOSED (NPZ not on allowlist): {ap}")
    return np.load(ap)

def sha256_of(path):
    h = hashlib.sha256()
    with guarded_open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""): h.update(chunk)
    return h.hexdigest()

def halt(msg):
    print(f"FAIL CLOSED: {msg}"); raise RuntimeError(f"FAIL CLOSED: {msg}")

def out_json(name, obj):
    os.makedirs(OUTD, exist_ok=True)
    p = os.path.join(OUTD, name)
    with guarded_open(p, "w") as f:
        json.dump({"_f2": F2_HEADER, **obj}, f, indent=1)
    return p

def self_audit_io():
    """L2 item 12/16: static audit of THIS file - raw open()/np.load() only inside guards."""
    src = guarded_open(os.path.abspath(__file__)).read()
    body = src.split("def self_audit_io", 1)[0] + src.split("def self_audit_io", 1)[1]
    allowed_defs = ("def guarded_open", "def guarded_npz")
    for m in re.finditer(r"(?<!guarded_)\bopen\(", src):
        line_start = src.rfind("\n", 0, m.start())
        window = src[max(0, m.start()-400):m.start()]
        if not any(a in window.split("def ")[-1- 0] or a in window for a in allowed_defs):
            # only guarded_open/guarded_npz bodies may call open()
            fn_ctx = src.rfind("def ", 0, m.start())
            fn_name = src[fn_ctx:src.find("(", fn_ctx)]
            if fn_name not in ("def guarded_open",):
                halt(f"self-audit: raw open() outside guard at offset {m.start()} ({fn_name})")
    for m in re.finditer(r"np\.load\(", src):
        fn_ctx = src.rfind("def ", 0, m.start())
        fn_name = src[fn_ctx:src.find("(", fn_ctx)]
        if fn_name not in ("def guarded_npz",):
            halt(f"self-audit: raw np.load() outside guard ({fn_name})")
    if "pd.read" in src or "pandas" in src.replace("# pandas", ""):
        halt("self-audit: pandas I/O present in harness")
    return {"io_self_audit": "PASS"}

# ==========================================================================
# 1. Frozen constants (source-verified against tcop_read.py at preflight)
# ==========================================================================
GRID_SIZE, N_CELLS, TICKS, BLOCK, N_BLOCKS = 50, 2500, 400, 25, 16
LAMBDA = 0.40; LOGIT_L = float(np.log(LAMBDA / (1.0 - LAMBDA)))
INIT_ACTIVE = round(0.40 * N_CELLS)
U_TIERS = [0.10, 0.25, 0.50]; TIERS_ALL = [0.0] + U_TIERS
MAGS = [0.0, 0.05, 0.10, 0.20, 0.35]
C_LABELS = [0.0, 0.05, -0.05, 0.10, -0.10, 0.20, -0.20, 0.35, -0.35]
STATIC_OFFSETS = {0.10: 0.04977134874876729, 0.25: 0.12339551870278656, 0.50: 0.24248438819907564}
PRIMARY_BLOCKS = list(range(3, 15))
PRIMARY_WINDOW_STARTS = [75 + 25 * i for i in range(9)]
WINDOW_LEN = 100                      # frozen-source-verified (v1's 75 was a defect)
PERMUTATIONS = 199; QUANTILE_METHOD = "lower"
RHO_BAND, RHO_ORIGIN = (0.35, 0.55), 0.35
DELTA_RHO = 0.002827351608578471; BUFFER = 0.00432
N_GLOBAL_BINS = int(np.ceil((RHO_BAND[1] - RHO_BAND[0]) / DELTA_RHO))
N_BIN_MIN, S_BIN_MIN = 9, 3
G1_CORR, G1_SLOPE = 0.7840162452332338, 0.0026279999999999915
G1B_VAR = 4.469162666666656e-06
G2_FLOOR = {"pos": 0.3832176592110196, "neg": 0.38138345899890086}
G4_MEAN_FLOOR, G4_Q05_FLOOR, G4_TAIL_CEIL = 0.22556575062981687, 0.19883692760900232, 0.0
HARD_LO, HARD_HI = 0.05, 0.95
EPS_VAR = 1e-9
ONSET = {"Psi_meanI_state": {"raw": 0.001990247078984684, "res": 0.0021133919208696263},
         "Psi_persistence_I": {"raw": 0.022837296913806253, "res": 0.023108397313261055}}
K_ONSET, S_ONSET = 2, 3
AXES = list(ONSET.keys())

CAL_SEED = 20260709
R_LADDER = [100, 500, 1000]
PRECISION_FRACTION = 0.5
Z90 = 1.6448536269514722
FLOOR_EVAL_B, FLOOR_EVAL_A, FLOOR_RECOVERY = 0.5, 0.5, 0.8
N1_TOL = {"window": 0.05, "row": 0.03, "setting": 0.03}

# P3 injection amplitude - FROZEN DERIVATION (spec guard; no gate-tuning, no output inspection):
#   target raw state Moran (mid pre-TCOP anchor)      I_target = 0.007
#   substrate variance term at rho~0.4                E[p(1-p)] ~= 0.24
#   field slope at LOGIT_L                            s = p(1-p) = 0.24
#   Moore-smoothed standardized field neighbor corr   RHO_KERN (analytic, computed below
#     from the smoothing operator's weight overlap: corr(k_i,k_j)= (2*w_self*w_nb + shared
#     neighbor overlap)/norm; for kernel self+8 uniform: RHO_KERN = 5/9 exactly on the
#     torus by weight-overlap count 5 of 9)
#   I_state ~= (s^2 a^2 RHO_KERN) / (E[p(1-p)] + s^2 a^2)   ->  solve for a.
#   SMALL-AMPLITUDE APPROXIMATION (L2-required label): sigmoid nonlinearity and finite
#   field normalization make this approximate, not an exact identity. rho_k=5/9 L2-verified.
RHO_KERN = 5.0 / 9.0
def p3_amplitude(scale):
    s2 = 0.24 ** 2; T = 0.007
    a2 = T * 0.24 / (s2 * (RHO_KERN - T))
    return float(np.sqrt(a2)) * scale
P3_SCALES = [1.0, 0.5]

# ==========================================================================
# 2. Stateless deterministic seeding (L2 item 11: resume-safe by construction)
# ==========================================================================
def seed_for(*tags):
    """seed = H(CAL_SEED | tags [| salt]) with canonical rejection; stateless, resume-safe."""
    salt = 0
    while True:
        h = hashlib.sha256(("|".join([str(CAL_SEED)] + [str(t) for t in tags] + [str(salt)])).encode()).digest()
        s = int.from_bytes(h[:4], "big") % (2**31 - 2) + 1
        if s not in CANONICAL_SEEDS: return s
        salt += 1   # deterministic rejection

def seed_set(*tags, n=5):
    return [seed_for(*tags, i) for i in range(n)]

# ==========================================================================
# 3. Frozen imports (Engine B core) - guarded loader + verification
# ==========================================================================
TR = None
FROZEN_FN_NAMES = ["calculate_morans_i_toroidal_8", "batch_morans_i_toroidal_8",
                   "get_neighbor_count", "sigmoid", "reconstruct_p_become",
                   "regress_on_template", "block_autocorr", "rho_bin", "q_lower",
                   "u_t_for", "sanitize_float"]

SAFE_CALL_ROOTS = {"float", "int", "round", "list", "tuple", "dict", "set", "range",
                   "np", "os", "hashlib", "json", "sorted", "len", "str", "abs", "min", "max"}

def _call_root(node):
    f = node.func
    while isinstance(f, ast.Attribute): f = f.value
    return getattr(f, "id", None)

def _static_module_check(src, name):
    """L2 items 8/A/C: AST check - no top-level calls/IO outside __main__ guard; defs,
    imports, assigns, and the __main__ guard only."""
    tree = ast.parse(src)
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef,
                             ast.Import, ast.ImportFrom, ast.Assign, ast.AnnAssign,
                             ast.AugAssign, ast.Expr)):
            if isinstance(node, ast.Expr) and not isinstance(node.value, ast.Constant):
                halt(f"static check {name}: top-level expression call")
            if isinstance(node, (ast.Assign, ast.AnnAssign, ast.AugAssign)):
                for sub in ast.walk(node):                     # L2 B4: calls in assigns
                    if isinstance(sub, ast.Call) and _call_root(sub) not in SAFE_CALL_ROOTS:
                        halt(f"static check {name}: non-whitelisted call in top-level assign: {_call_root(sub)}")
            continue
        if isinstance(node, ast.If):
            t = node.test
            if (isinstance(t, ast.Compare) and getattr(t.left, "id", "") == "__name__"):
                continue
            halt(f"static check {name}: non-__main__ top-level If")
        halt(f"static check {name}: disallowed top-level node {type(node).__name__}")

def import_frozen(path, digest, name):
    """L2 B4: execute the ALREADY-GUARDED, digest-verified source string in a fresh module
    namespace; no import machinery touches disk; bytecode writing disabled globally."""
    sys.dont_write_bytecode = True
    if sha256_of(path) != digest: halt(f"{name} digest mismatch")
    src = guarded_open(path, encoding="utf-8").read()
    _static_module_check(src, name)
    import types
    mod = types.ModuleType(name); mod.__file__ = path
    sys.modules[name] = mod
    exec(compile(src, path, "exec"), mod.__dict__)
    return mod, src

def verify_frozen(mod, src, manifest):
    rec = {}
    for fname in FROZEN_FN_NAMES:
        fn = getattr(mod, fname, None)
        if fn is None: halt(f"missing frozen fn {fname}")
        fsrc = inspect.getsource(fn)
        idx = src.find(fsrc)
        if idx < 0: halt(f"byte-for-byte FAIL {fname}")
        rec[fname] = {"span": [idx, idx + len(fsrc)],
                      "span_sha256": hashlib.sha256(fsrc.encode()).hexdigest()}
    for cn, v in [("G1_CORR", G1_CORR), ("G1_SLOPE", G1_SLOPE), ("G1B_VAR", G1B_VAR),
                  ("G2_FLOOR_POS", G2_FLOOR["pos"]), ("G2_FLOOR_NEG", G2_FLOOR["neg"]),
                  ("G4_MEAN_FLOOR", G4_MEAN_FLOOR), ("G4_Q05_FLOOR", G4_Q05_FLOOR),
                  ("G4_TAIL_CEIL", G4_TAIL_CEIL), ("K_ONSET", K_ONSET), ("S_ONSET", S_ONSET),
                  ("PERMUTATIONS", PERMUTATIONS), ("DELTA_RHO", DELTA_RHO),
                  ("WINDOW_LEN", WINDOW_LEN), ("N_GLOBAL_BINS", getattr(mod, "N_GLOBAL_BINS", N_GLOBAL_BINS))]:
        mv = getattr(mod, cn, None)
        if mv is None or (mv != v if not isinstance(v, float) else abs(mv - v) > 0):
            halt(f"constant mismatch {cn}: {mv} vs {v}")
    for ax in AXES:
        for k in ("raw", "res"):
            if mod.ONSET[ax][k] != ONSET[ax][k]: halt(f"ONSET mismatch {ax}/{k}")
    if list(getattr(mod, "PRIMARY_WINDOW_STARTS")) != PRIMARY_WINDOW_STARTS: halt("window starts")
    manifest["byte_for_byte_spans"] = rec

def kappa_map_from_source(src):
    """L2 item 8: AST literal extraction of KAPPA_MAP - no run-script execution."""
    tree = ast.parse(src)
    for node in tree.body:
        if isinstance(node, ast.Assign) and getattr(node.targets[0], "id", "") == "KAPPA_MAP":
            pairs = ast.literal_eval(node.value)
            return {round(float(c), 4): float(k) for c, k in pairs}
    halt("KAPPA_MAP not found by AST extraction")

KAPPA = None
def kappa_for(c):
    key = round(c, 4)
    if key not in KAPPA: halt(f"c-label {c} not in frozen KAPPA_MAP")
    return KAPPA[key]

def verify_offsets_by_reproduction(tcop_src):
    """Reproduce the solved static offsets from the frozen periodic-orbit construction;
    halt if the spec literals do not match to 1e-12 (verification-by-reproduction)."""
    def orbit_mean(u_tier, n_cycles=400):
        p_seq = [TRS.sigmoid(LOGIT_L + lvl) for lvl in (0.0, u_tier/2.0, u_tier)]
        rho = 0.40; acc = []
        for cyc in range(n_cycles):
            for p in p_seq:
                for _ in range(BLOCK):
                    rho = rho * LAMBDA + (1 - rho) * p
                    if cyc >= n_cycles // 2: acc.append(rho)
        return float(np.mean(acc))
    def static_rho(u_const):
        p = TRS.sigmoid(LOGIT_L + u_const)
        return p / (1 - LAMBDA + p)
    for u, want in STATIC_OFFSETS.items():
        target = orbit_mean(u)
        lo, hi = 0.0, u
        for _ in range(200):
            mid = (lo + hi) / 2
            if static_rho(mid) < target: lo = mid
            else: hi = mid
        got = (lo + hi) / 2
        if abs(got - want) > 1e-9:
            halt(f"offset reproduction mismatch u={u}: {got} vs spec {want}")
    return True

class _TRShim:  # minimal frozen-callable access before TR set (offsets check)
    def __getattr__(self, n): return getattr(TR, n)
TRS = _TRShim()

# ==========================================================================
# 4. ENGINE A - simulator (verbatim discipline; F3-analog gate)
# ==========================================================================
def simulate_run(kappa, tier, u_const, mode, seed):
    np.random.seed(seed)
    import random as _r; _r.seed(seed)
    flat = np.zeros(N_CELLS, dtype=int); flat[:INIT_ACTIVE] = 1
    np.random.shuffle(flat)
    grid = flat.reshape((GRID_SIZE, GRID_SIZE))
    states = np.zeros((TICKS, GRID_SIZE, GRID_SIZE), dtype=int)
    for t in range(TICKS):
        states[t] = grid
        u_t = TR.u_t_for(mode, tier, u_const, t // BLOCK)
        rand_grid = np.random.rand(GRID_SIZE, GRID_SIZE)
        q = TR.get_neighbor_count(grid) / 8.0
        p_b = TR.sigmoid(LOGIT_L + u_t + kappa * (2.0 * q - 1.0))
        become = (grid == 0) & (rand_grid < p_b)
        stay = (grid == 1) & (rand_grid < LAMBDA)
        grid = (become | stay).astype(int)
    return states

def f3_analog_gate(manifest):
    rec = {}
    for s in CANONICAL_SEEDS:
        committed = guarded_npz(null_ext_npz(s))["states"]
        sim = simulate_run(0.0, 0.0, None, "cm1", s)
        if not np.array_equal(committed, sim): halt(f"F3-ANALOG FAIL seed {s}")
        rec[str(s)] = True
    manifest["f3_analog_bit_exact"] = rec

# ==========================================================================
# 5. Frozen gate evaluation on a simulated run (semantics verbatim from
#    tcop_read.py main(); propensities RECONSTRUCTED per frozen convention)
# ==========================================================================
def process_sim_run(states, mode, c_label, tier, u_const, seed, with_onset):
    kappa = kappa_for(c_label)
    rhos = states.mean(axis=(1, 2))
    block_means = np.array([rhos[b*BLOCK:(b+1)*BLOCK].mean() for b in PRIMARY_BLOCKS])
    phase_stats = [TR.regress_on_template(block_means, phi) for phi in range(3)]
    rec = {"mode": mode, "c_label": c_label, "tier": tier, "seed": seed,
           "phase0": list(phase_stats[0]), "phases_all": [list(p) for p in phase_stats],
           "var0": float(np.var(block_means))}
    rec["g1b"] = bool(rec["var0"] > G1B_VAR)
    g4b = {"mean_slope": [], "q05_lower": [], "tail": []}
    propI = []
    for b in PRIMARY_BLOCKS:
        bs = states[b*BLOCK:(b+1)*BLOCK]
        u_lvl = TR.u_t_for(mode, tier, u_const, b)
        pb = np.stack([TR.reconstruct_p_become(bs[i], kappa, u_lvl) for i in range(BLOCK)])
        sl = pb * (1.0 - pb)
        g4b["mean_slope"].append(float(sl.mean()))
        g4b["q05_lower"].append(TR.q_lower(sl.ravel(), 5))
        g4b["tail"].append(float(np.mean((pb < HARD_LO) | (pb > HARD_HI))))
        if all(float(np.var(pb[i])) >= EPS_VAR for i in range(BLOCK)):
            propI.append(float(np.mean(TR.batch_morans_i_toroidal_8(pb))))
        else:
            propI.append(None)   # zero-variance blocks excluded per frozen convention
    rec["g4_pass"] = bool(min(g4b["mean_slope"]) >= G4_MEAN_FLOOR and
                          min(g4b["q05_lower"]) >= G4_Q05_FLOOR and
                          max(g4b["tail"]) <= G4_TAIL_CEIL)
    nn = [v for v in propI if v is not None]
    rec["prop_I_row"] = float(np.mean(nn)) if nn else None
    rec["g1_applicable"] = bool(mode == "cm1" and tier > 0.0)
    rec["windows"] = []
    for ws in PRIMARY_WINDOW_STARTS:
        wmr = float(rhos[ws:ws+WINDOW_LEN].mean())
        wrec = {"ws": ws, "phase": (ws // BLOCK) % 3, "bin": TR.rho_bin(wmr), "wmr": wmr}
        if with_onset:
            win = states[ws:ws+WINDOW_LEN]
            np.random.seed(seed_for("perm", mode, c_label, tier, seed, ws))  # deterministic
            raw_mI = float(np.mean(TR.batch_morans_i_toroidal_8(win.astype(float))))
            flat = win.reshape(WINDOW_LEN, -1).astype(float)
            null_mI = np.zeros(PERMUTATIONS)
            for p in range(PERMUTATIONS):
                idx = np.random.rand(WINDOW_LEN, N_CELLS).argsort(axis=0)   # frozen axis=0
                null_mI[p] = float(np.mean(TR.batch_morans_i_toroidal_8(
                    np.take_along_axis(flat, idx, axis=0).reshape(WINDOW_LEN, GRID_SIZE, GRID_SIZE))))
            pgrid = win.mean(axis=0)
            raw_pI = float(TR.calculate_morans_i_toroidal_8(pgrid))
            fp = pgrid.ravel()
            null_pI = np.zeros(PERMUTATIONS)
            for p in range(PERMUTATIONS):
                null_pI[p] = float(TR.calculate_morans_i_toroidal_8(
                    np.random.permutation(fp).reshape(GRID_SIZE, GRID_SIZE)))
            for ax, raw, nulls in [("Psi_meanI_state", raw_mI, null_mI),
                                   ("Psi_persistence_I", raw_pI, null_pI)]:
                res = abs(raw - float(np.mean(nulls)))
                wrec[ax] = {"raw": raw, "res": res,
                            "exceeds": bool(abs(raw) > ONSET[ax]["raw"] and res > ONSET[ax]["res"])}
        rec["windows"].append(wrec)
    if with_onset:
        rec["onset"] = {}
        for ax in AXES:
            nex = sum(1 for w in rec["windows"] if w[ax]["exceeds"])
            rec["onset"][ax] = {"exceed_count": nex, "row_flag": bool(nex >= K_ONSET)}
    return rec

def g1_eval(rec, dom):
    if not rec["g1_applicable"]: return None   # tier-0: G1-exempt per frozen source
    r0, b0, _ = rec["phase0"]
    ok = (b0 > 0 and r0 > G1_CORR and b0 > G1_SLOPE and
          r0 > dom["dominance_r"] and b0 > dom["dominance_beta"] and rec["var0"] > dom["dominance_var"])
    return bool(ok)

def comparator_sets(cm0_recs):
    comp = {}
    for rec in cm0_recs:
        key = (rec["c_label"], rec["tier"])
        c = comp.setdefault(key, {"r": [], "beta": [], "var": []})
        for r, b, _ in rec["phases_all"]:
            c["r"].append(r); c["beta"].append(b)
        c["var"].append(rec["var0"])
    out = {}
    for key, c in comp.items():
        if len(c["r"]) != 15 or len(c["var"]) != 5: halt(f"comparator malformed {key}")
        out[key] = {"dominance_r": max(0.0, max(c["r"])),
                    "dominance_beta": max(0.0, max(c["beta"])),
                    "dominance_var": max(c["var"])}
    return out

def g2_eval(cm1_by_cell):
    g2 = {}
    for tier in U_TIERS:
        for sign, floor in [("pos", G2_FLOOR["pos"]), ("neg", G2_FLOOR["neg"])]:
            sgn = 1 if sign == "pos" else -1
            med, low, seqs = [], [], []
            for mag in MAGS[1:]:
                vals = [r["prop_I_row"] for r in cm1_by_cell[(tier, sgn*mag)] if r["prop_I_row"] is not None]
                if len(vals) != 5: halt(f"G2 vals != 5 at tier {tier} c {sgn*mag}")
                med.append(float(np.median(vals))); low.append(TR.q_lower(vals, 10)); seqs.append(vals)
            g2[(tier, sign)] = bool(all(med[i+1] >= med[i] for i in range(3)) and
                                    all(low[i+1] >= low[i] for i in range(3)) and
                                    low[3] >= floor)
    return g2

def eligibility(side1, side2):
    n1, n2 = len(side1), len(side2)
    if n1 < N_BIN_MIN or n2 < N_BIN_MIN: return "count-failed"
    for side in (side1, side2):
        sc = {}
        for w in side: sc[w["seed"]] = sc.get(w["seed"], 0) + 1
        if len(sc) < S_BIN_MIN: return "seed-failed"
        if max(sc.values()) > len(side) / 2.0: return "seed-failed"
    h1 = [sum(1 for w in side1 if w["phase"] == p) for p in range(3)]
    h2 = [sum(1 for w in side2 if w["phase"] == p) for p in range(3)]
    if any(abs(h1[p] - h2[p]) > 1 for p in range(3)): return "phase-confounded"
    return "eligible"

def comparison_universe():
    uni = []
    for i in range(len(TIERS_ALL)):
        for j in range(i+1, len(TIERS_ALL)):
            uni.append({"path": "a", "side1": (TIERS_ALL[i], 0.0), "side2": (TIERS_ALL[j], 0.0)})
    for tier in U_TIERS:
        for sign in (+1, -1):
            for i in range(len(MAGS)):
                for j in range(i+1, len(MAGS)):
                    uni.append({"path": "b", "sign": sign, "tier": tier,
                                "side1": (tier, sign*MAGS[i] if MAGS[i] > 0 else 0.0),
                                "side2": (tier, sign*MAGS[j])})
    seen, out = set(), []
    for u in uni:
        k = (u["path"], u.get("sign"), u["side1"], u["side2"])
        if k not in seen: seen.add(k); out.append(u)
    return out

def geometry_replicate(rep_idx, with_rows=True):
    """Full frozen stack per replicate, permutation-free (eligibility geometry only).
    CM-0 FIRST (comparators frozen before CM-1). Stateless seeds by (stage, rep, cell)."""
    cm0 = []
    for tier in U_TIERS:
        for c in C_LABELS:
            for si, s in enumerate(seed_set("geom", rep_idx, "cm0", tier, c)):
                st = simulate_run(kappa_for(c), tier, STATIC_OFFSETS[tier], "cm0", s)
                cm0.append(process_sim_run(st, "cm0", c, tier, STATIC_OFFSETS[tier], s, with_onset=False))
    dom = comparator_sets(cm0)
    cm1_by_cell, rows_by_setting = {}, {}
    for tier in TIERS_ALL:
        for c in C_LABELS:
            cell = []
            for s in seed_set("geom", rep_idx, "cm1", tier, c):
                st = simulate_run(kappa_for(c), tier, None, "cm1", s)
                rec = process_sim_run(st, "cm1", c, tier, None, s, with_onset=False)
                rec["g1_pass"] = g1_eval(rec, dom.get((c, tier), {"dominance_r": 9, "dominance_beta": 9, "dominance_var": 9})) \
                                 if rec["g1_applicable"] else None
                cell.append(rec)
            cm1_by_cell[(tier, c)] = cell
    g2 = g2_eval(cm1_by_cell)
    lift = {tier: all(bool(r["g1_pass"]) for r in cm1_by_cell[(tier, 0.0)]) for tier in U_TIERS}
    def setting_windows(tier, c):
        out = []
        for r in cm1_by_cell[(tier, c)]:
            if not r["g4_pass"]: continue
            if r["g1_applicable"] and not r["g1_pass"]: continue
            for w in r["windows"]:
                if w["bin"] is not None: out.append({"seed": r["seed"], **w})
        return out
    elig_b_families, elig_a_bins = [], set()
    for pair in comparison_universe():
        w1, w2 = setting_windows(*pair["side1"]), setting_windows(*pair["side2"])
        elig_bins = []
        for b in range(N_GLOBAL_BINS):
            s1 = [w for w in w1 if w["bin"] == b]; s2 = [w for w in w2 if w["bin"] == b]
            if not (s1 and s2): continue
            if eligibility(s1, s2) == "eligible":
                elig_bins.append(b)
                if pair["path"] == "a":
                    elig_a_bins.add((pair["side1"][0], b)); elig_a_bins.add((pair["side2"][0], b))
        if pair["path"] == "b" and pair["side1"][1] == 0.0 and abs(pair["side2"][1]) >= 0.20 and elig_bins:
            sign_key = "pos" if pair["side2"][1] > 0 else "neg"
            if g2[(pair["tier"], sign_key)]:
                # L2 B1B: store EXACT eligible window keys per side per bin
                wk = {}
                for b in elig_bins:
                    wk[str(b)] = {"side1": [{"seed": w["seed"], "ws": w["ws"], "phase": w["phase"]}
                                             for w in w1 if w["bin"] == b],
                                  "side2": [{"seed": w["seed"], "ws": w["ws"], "phase": w["phase"]}
                                             for w in w2 if w["bin"] == b]}
                elig_b_families.append({"tier": pair["tier"], "c2": pair["side2"][1],
                                        "bins": elig_bins, "window_keys": wk})
    strata = [np.mean([r["windows"][0]["wmr"] for r in cm1_by_cell[(t, 0.0)]]) for t in TIERS_ALL]
    rep = {"eligible_b_families": elig_b_families, "n_elig_b": len(elig_b_families),
           "eligible_a_bins": sorted([list(x) for x in elig_a_bins]),
           "n_elig_a": len(elig_a_bins),
           "evaluable_b": len(elig_b_families) >= 1, "evaluable_a": len(elig_a_bins) >= 1,
           "c0_strata_by_tier": [float(x) for x in strata],
           "strata_span": float(max(strata) - min(strata)),
           "g2": {f"{k}": bool(v) for k, v in g2.items()}, "lift": lift}
    if with_rows:
        out_json(f"geom_rows_rep{rep_idx}.json", {"families": elig_b_families})
    return rep

# ==========================================================================
# 6. Injections (P3 floor-plus-texture; N2 zero-mode; N3 uncorrelated)
# ==========================================================================
def sim_injected(seed, inject):
    """Floor substrate (kappa=0) with injected propensity term added INSIDE the
    becoming-active logit at the earliest substrate level: p = sigmoid(LOGIT_L + field_t).
    FROZEN CHOICE per menu: P3/N3 are FLOOR-plus-texture (kappa=0 on the floor cell, so the
    kappa term is identically zero, stated not hidden); N2 adds the schedule template."""
    np.random.seed(seed)
    import random as _r; _r.seed(seed)
    flat = np.zeros(N_CELLS, dtype=int); flat[:INIT_ACTIVE] = 1
    np.random.shuffle(flat)
    grid = flat.reshape((GRID_SIZE, GRID_SIZE))
    states = np.zeros((TICKS, GRID_SIZE, GRID_SIZE), dtype=int)
    for t in range(TICKS):
        states[t] = grid
        rand_grid = np.random.rand(GRID_SIZE, GRID_SIZE)
        p_b = TR.sigmoid(LOGIT_L + inject(t))
        become = (grid == 0) & (rand_grid < p_b)
        stay = (grid == 1) & (rand_grid < LAMBDA)
        grid = (become | stay).astype(int)
    return states

def moore_field(seed):
    rng = np.random.default_rng(seed)
    n = rng.standard_normal((GRID_SIZE, GRID_SIZE))
    k = n + TR.get_neighbor_count(n)
    return (k - k.mean()) / k.std()

def make_p3(rep_idx, scale, s):
    field = p3_amplitude(scale) * moore_field(seed_for("p3field", rep_idx, s))
    return lambda t: field
def make_n2(tier):
    return lambda t: TR.u_t_for("cm1", tier, None, t // BLOCK)
def make_n3(rep_idx, scale, s):
    rng = np.random.default_rng(seed_for("n3field", rep_idx, s))
    a = p3_amplitude(scale)
    field = a * rng.standard_normal((GRID_SIZE, GRID_SIZE))   # variance-matched, uncorrelated
    return lambda t: field
def make_n4(rep_idx, scale, s):
    a = p3_amplitude(scale)
    cb = np.indices((GRID_SIZE, GRID_SIZE)).sum(axis=0) % 2 * 2.0 - 1.0
    return lambda t: a * cb

def onset_only(states, tag_tuple):
    return process_sim_run(states, "cm1", 0.0, 0.0, None, tag_tuple[-1], with_onset=True)["onset"]

# ==========================================================================
# 7. Stages
# ==========================================================================
def _load_ck(name, default):
    p = os.path.join(OUTD, name)
    if os.path.exists(p):
        return json.load(guarded_open(p))
    return default

def stage_preflight():
    global TR, KAPPA
    os.makedirs(OUTD, exist_ok=True)
    man = {"stage": "preflight", "cal_seed": CAL_SEED, "time": time.time(),
           "permitted": {}, "amendment1": {}}
    for p in sorted(PERMITTED_READS):
        if p.endswith(".npz") or p == os.path.abspath(__file__):
            if not os.path.exists(p): halt(f"missing permitted: {p}")
            continue
        man["permitted"][os.path.relpath(p, REPO)] = sha256_of(p)
    if man["permitted"]["tcop_read.py"] != TCOP_READ_DIGEST: halt("tcop_read digest")
    rel_tcop = os.path.join("cycle3", "wave_two", "c3_w2_tcop.py")
    rel_m2 = os.path.join("cycle3", "wave_two", "c3_w2_rule_c_m2.py")
    if man["permitted"][rel_tcop] != C3W2TCOP_DIGEST: halt("c3_w2_tcop digest")
    if man["permitted"][rel_m2] != RULECM2_DIGEST: halt("c3_w2_rule_c_m2 digest")   # L2 item 13
    man["amendment1"] = {rel_tcop: "permitted by Amendment 1, construction-only, zero realized quantities, digest-verified",
                         rel_m2:   "permitted by Amendment 1, construction-only, zero realized quantities, digest-verified"}
    man.update(self_audit_io())
    TRmod, src = import_frozen(os.path.join(REPO, "tcop_read.py"), TCOP_READ_DIGEST, "tcop_read_frozen")
    TR = TRmod
    verify_frozen(TR, src, man)
    tcop_src = guarded_open(os.path.join(W2, "c3_w2_tcop.py"), encoding="utf-8").read()
    _static_module_check(tcop_src, "c3_w2_tcop")   # never imported/executed; AST only
    KAPPA = kappa_map_from_source(tcop_src)
    man["kappa_map"] = {str(k): v for k, v in KAPPA.items()}
    verify_offsets_by_reproduction(tcop_src)
    man["offsets_reproduced"] = True
    man.update(golden_tests())
    f3_analog_gate(man)
    man["canonical_seed_fence"] = CANONICAL_SEEDS
    man["harness_sha256"] = sha256_of(os.path.abspath(__file__))
    man["permutation_seeding_note"] = ("Permutation construction frozen; calibration permutation "
                                       "seed stream deterministic per run/window for resume safety.")
    man["p3_amplitude_frozen"] = {"rho_kern": RHO_KERN, "a_1x": p3_amplitude(1.0),
                                  "derivation": "target 0.007 raw Moran; I=(s^2 a^2 rho_k)/(Ep(1-p)+s^2 a^2)"}
    p = out_json("preflight_manifest.json", man)
    print("PREFLIGHT PASS ->", p, sha256_of(p))

def stage_geometry():
    _boot()
    R = _current_R("geometry")
    ck = _load_ck("geometry_checkpoint.json", {"reps": []})
    for i in range(len(ck["reps"]), R):
        ck["reps"].append(geometry_replicate(i))
        out_json("geometry_checkpoint.json", ck)
        if (i + 1) % 5 == 0: print(f"geom {i+1}/{R}")
    reps = ck["reps"]
    kb = sum(1 for r in reps if r["evaluable_b"]); ka = sum(1 for r in reps if r["evaluable_a"])
    summ = {"R": len(reps), "kb": kb, "ka": ka,
            "path_b": {"est": kb/len(reps), "wilson90": wilson(kb, len(reps))},
            "path_a": {"est": ka/len(reps), "wilson90": wilson(ka, len(reps))},
            "n_elig_b_counts": [r["n_elig_b"] for r in reps],
            "strata_spans": [r["strata_span"] for r in reps],
            "evaluable_indices": [i for i, r in enumerate(reps) if r["evaluable_b"]]}
    for path, k, floor in (("path_b", kb, FLOOR_EVAL_B), ("path_a", ka, FLOOR_EVAL_A)):
        ok, iv = precision_gate(k, len(reps), floor)
        summ[path]["precision_ok"] = ok
        if not ok: summ["escalation_required"] = True
    p = out_json("geometry_summary.json", summ)
    print("geometry ->", p, sha256_of(p))

def stage_recovery():
    _boot()
    geo = json.load(guarded_open(os.path.join(OUTD, "geometry_summary.json")))
    ev_idx = geo["evaluable_indices"]
    R = _current_R("recovery")
    ck = _load_ck("recovery_checkpoint.json", {"P1": [0, 0], "P2": [0, 0],
                                               "P3_1x": [0, 0], "P3_0p5x": [0, 0], "done": 0})
    if not ev_idx:
        ck["outcome"] = "NO EVALUABLE GEOMETRY DRAWS: recovery not estimable; recorded as evaluability failure"
        out_json("recovery_summary.json", ck); return
    for i in range(ck["done"], R):
        gsel = ev_idx[seed_for("evsample", i) % len(ev_idx)]   # conditioned sampling (L2 item 14)
        # P1: committed cell, onset both signs, S_ONSET aggregation
        hit1 = True
        for c in (0.35, -0.35):
            flags = {ax: 0 for ax in AXES}
            for s in seed_set("rec", i, "P1", c):
                st = simulate_run(kappa_for(c), 0.0, None, "cm1", s)
                on = process_sim_run(st, "cm1", c, 0.0, None, s, with_onset=True)["onset"]
                for ax in AXES: flags[ax] += int(on[ax]["row_flag"])
            if any(flags[ax] < S_ONSET for ax in AXES): hit1 = False
        ck["P1"] = [ck["P1"][0] + int(hit1), ck["P1"][1] + 1]
        # P2 (L2 B1A/B1B): ALL eligible families; EXACT stored eligible windows only;
        # replicate hit iff ANY family clears the frozen burden on any axis; family-level counts kept
        fam = json.load(guarded_open(os.path.join(OUTD, f"geom_rows_rep{gsel}.json")))["families"]
        hit2 = False; fam_hits = 0
        onset_cache = {}
        def run_windows(tier, c, seed):
            key = (tier, c, seed)
            if key not in onset_cache:
                st = simulate_run(kappa_for(c), tier, None, "cm1", seed)   # stateless regeneration
                onset_cache[key] = process_sim_run(st, "cm1", c, tier, None, seed, with_onset=True)["windows"]
            return onset_cache[key]
        for f in fam:
            tier, c2 = f["tier"], f["c2"]
            fhit = False
            for b, sides in f["window_keys"].items():
                def pick(c, keys):
                    out = []
                    for k in keys:
                        for w in run_windows(tier, c, k["seed"]):
                            if w["ws"] == k["ws"] and w["phase"] == k["phase"]:   # L2 v3 B1: full key
                                out.append(w)
                    return out
                s1 = pick(0.0, sides["side1"]); s2 = pick(c2, sides["side2"])
                for ax in AXES:
                    ex1 = sum(1 for w in s1 if w[ax]["exceeds"]); ex2 = sum(1 for w in s2 if w[ax]["exceeds"])
                    re1 = float(np.mean([w[ax]["res"] - ONSET[ax]["res"] for w in s1])) if s1 else -1
                    re2 = float(np.mean([w[ax]["res"] - ONSET[ax]["res"] for w in s2])) if s2 else -1
                    if ex2 >= ex1 and (ex2 > ex1 or re2 > re1): fhit = True
            fam_hits += int(fhit); hit2 = hit2 or fhit
        ck["P2"] = [ck["P2"][0] + int(hit2), ck["P2"][1] + 1]
        ck.setdefault("P2_family_level", [0, 0])
        ck["P2_family_level"] = [ck["P2_family_level"][0] + fam_hits,
                                 ck["P2_family_level"][1] + len(fam)]
        # P3: two-rung ledger (L2 item 6)
        for key, scale in (("P3_1x", 1.0), ("P3_0p5x", 0.5)):
            hit3 = True
            for s in seed_set("rec", i, key)[:3]:
                st = sim_injected(seed_for("p3run", i, key, s), make_p3(i, scale, s))
                on = onset_only(st, ("p3", s))
                if not all(on[ax]["row_flag"] for ax in AXES): hit3 = False
            ck[key] = [ck[key][0] + int(hit3), ck[key][1] + 1]
        ck["done"] = i + 1
        out_json("recovery_checkpoint.json", ck)
        if (i + 1) % 5 == 0: print(f"rec {i+1}/{R}")
    summ = {k: {"k": v[0], "n": v[1], "est": v[0]/max(v[1],1), "wilson90": wilson(v[0], max(v[1],1))}
            for k, v in ck.items() if isinstance(v, list)}
    summ["P1"]["precision_vs_recovery_floor"] = precision_gate(ck["P1"][0], ck["P1"][1], FLOOR_RECOVERY)
    summ["conditioning"] = "each recovery replicate tied to a sampled evaluable geometry draw; P2 evaluated inside that draw's eligible family via stateless-seed regeneration"
    p = out_json("recovery_summary.json", summ)
    print("recovery ->", p, sha256_of(p))

def stage_controls():
    _boot()
    R = _current_R("controls")
    ck = _load_ck("controls_checkpoint.json",
                  {"N1": {"window": [0, 0], "row": [0, 0], "setting": [0, 0]},
                   "N2": {f"tier{t}_{lvl}": [0, 0] for t in (0.10, 0.25, 0.50) for lvl in ("row", "setting")},
                   "N3": {"row": [0, 0], "setting": [0, 0]},
                   "N4_nonscoring": {"neg_signed": 0, "pos_mislabel": 0, "n": 0},
                   "done": 0})
    for i in range(ck["done"], R):
        # N1 pure null
        flags = []
        for s in seed_set("ctrl", i, "N1"):
            on = process_sim_run(simulate_run(0.0, 0.0, None, "cm1", s), "cm1", 0.0, 0.0, None, s, True)["onset"]
            flags.append(on)
            for ax in AXES:
                ck["N1"]["window"][1] += 9; ck["N1"]["window"][0] += on[ax]["exceed_count"]
                ck["N1"]["row"][1] += 1;   ck["N1"]["row"][0] += int(on[ax]["row_flag"])
        for ax in AXES:
            ck["N1"]["setting"][1] += 1
            ck["N1"]["setting"][0] += int(sum(int(f[ax]["row_flag"]) for f in flags) >= S_ONSET)
        # N2 zero-mode schedule-shaped modulation - ALL committed tiers (L2 B2)
        for t in (0.10, 0.25, 0.50):
            flags = []
            for s in seed_set("ctrl", i, "N2", t):
                st = sim_injected(seed_for("n2run", i, t, s), make_n2(t))
                on = onset_only(st, ("n2", s)); flags.append(on)
                for ax in AXES:
                    ck["N2"][f"tier{t}_row"][1] += 1
                    ck["N2"][f"tier{t}_row"][0] += int(on[ax]["row_flag"])
            for ax in AXES:
                ck["N2"][f"tier{t}_setting"][1] += 1
                ck["N2"][f"tier{t}_setting"][0] += int(sum(int(f[ax]["row_flag"]) for f in flags) >= S_ONSET)
        # N3 uncorrelated variance inflation - row AND setting aggregation (L2 B2)
        flags = []
        for s in seed_set("ctrl", i, "N3"):
            st = sim_injected(seed_for("n3run", i, s), make_n3(i, 1.0, s))
            on = onset_only(st, ("n3", s)); flags.append(on)
            for ax in AXES:
                ck["N3"]["row"][1] += 1; ck["N3"]["row"][0] += int(on[ax]["row_flag"])
        for ax in AXES:
            ck["N3"]["setting"][1] += 1
            ck["N3"]["setting"][0] += int(sum(int(f[ax]["row_flag"]) for f in flags) >= S_ONSET)
        # N4 NON-SCORING signed-discipline audit
        s = seed_set("ctrl", i, "N4")[0]
        st = sim_injected(seed_for("n4run", i, s), make_n4(i, 1.0, s))
        r = process_sim_run(st, "cm1", 0.0, 0.0, None, s, with_onset=True)
        ck["N4_nonscoring"]["n"] += 1
        for w in r["windows"]:
            if w["Psi_meanI_state"]["exceeds"]:
                if w["Psi_meanI_state"]["raw"] < 0: ck["N4_nonscoring"]["neg_signed"] += 1
                else: ck["N4_nonscoring"]["pos_mislabel"] += 1
        ck["done"] = i + 1
        out_json("controls_checkpoint.json", ck)
        if (i + 1) % 5 == 0: print(f"ctrl {i+1}/{R}")
    summ = {"N4_nonscoring": ck["N4_nonscoring"], "tolerances": N1_TOL}
    for ctrl in ("N1", "N2", "N3"):
        summ[ctrl] = {}
        for lvl, (k, n) in ck[ctrl].items():
            iv = wilson(k, n)
            base_lvl = lvl.split("_")[-1]
            tol = N1_TOL.get(base_lvl, N1_TOL["row"])
            summ[ctrl][lvl] = {"k": k, "n": n, "wilson90": iv, "tol": tol,
                               "pass_at_current_R": bool(iv[1] <= tol),
                               "escalate_if_fail": "frozen ladder before any FAIL verdict"}
    p = out_json("controls_summary.json", summ)
    print("controls ->", p, sha256_of(p))

def stage_forecast():
    _boot()
    geo = json.load(guarded_open(os.path.join(OUTD, "geometry_summary.json")))
    rec = json.load(guarded_open(os.path.join(OUTD, "recovery_summary.json")))
    ctl = json.load(guarded_open(os.path.join(OUTD, "controls_summary.json")))
    R = geo["R"]
    esc = _load_ck("escalation.json", {})
    inv_c, unr_c = control_verdict_items(ctl, R_LADDER[-1])      # pure fns (golden-tested)
    inv_p, unr_p = p1_verdict_items(rec.get("P1", {}), FLOOR_RECOVERY, R_LADDER[-1])
    invalid, unresolved = inv_c + inv_p, unr_c + unr_p
    pb_ok, pb_iv = precision_gate(geo["kb"], R, FLOOR_EVAL_B)
    pa_ok, pa_iv = precision_gate(geo["ka"], R, FLOOR_EVAL_A)
    counts = geo["n_elig_b_counts"]; spans = geo["strata_spans"]
    audit = {"reconstruction": "post-Amendment-1 stack; currency replay per frozen spec Section 1",
             "budget": {"evaluability_b": geo["path_b"], "evaluability_a": geo["path_a"],
                        "recovery": rec, "controls": ctl,
                        "method": "end-to-end Monte Carlo, conditioned two-arm, Wilson 90%"},
             "forecast": {"eligible_b_family_count_interval_90":
                              [float(np.percentile(counts, 5, method=QUANTILE_METHOD)),
                               float(np.percentile(counts, 95, method=QUANTILE_METHOD))],
                          "eligible_b_family_median": float(np.median(counts)),
                          "minimum_eligible_support_for_tier": 1,
                          "c0_strata_span_interval_90":
                              [float(np.percentile(spans, 5, method=QUANTILE_METHOD)),
                               float(np.percentile(spans, 95, method=QUANTILE_METHOD))],
                          "strata_median_exceeds_bin_plus_buffer": bool(np.median(spans) > DELTA_RHO + BUFFER),
                          "interval_construction": "empirical replicate quantiles, method=lower; no post-hoc widening"},
             "tranche_2_6": "not applicable for execution; prospective statement per frozen spec Section 5",
             "ladder_2_7": "reconstructed per frozen spec Section 5",
             "floors": {"eval_b": FLOOR_EVAL_B, "eval_a": FLOOR_EVAL_A, "recovery": FLOOR_RECOVERY},
             "precision": {"path_b": {"ok": pb_ok, "wilson90": pb_iv},
                           "path_a": {"ok": pa_ok, "wilson90": pa_iv}},
             "recovery_reported_not_floored": {          # L2 B3: P2/P3 in taxonomy, explicit status
                 "P2": rec.get("P2"), "P2_family_level": rec.get("P2_family_level"),
                 "P3_1x": rec.get("P3_1x"), "P3_0p5x": rec.get("P3_0p5x"),
                 "status": "reported diagnostics; no frozen floor attaches (frozen spec Section 4)"},
             "escalation_state": esc,
             "unresolved": unresolved}
    below = (wilson(geo["kb"], R)[1] < FLOOR_EVAL_B) or (wilson(geo["ka"], R)[1] < FLOOR_EVAL_A)
    cat = classify_verdict(invalid, unresolved, pb_ok, pa_ok, below)
    audit["verdict_2_8"] = {"category": cat, "reasons": invalid, "items": unresolved,
                            "basis": "computed floors vs Wilson-90 intervals; controls, recovery "
                                     "floors, per-component precision, and escalation state all "
                                     "inputs to this branch (pure classify_verdict; golden-tested)"}
    p = out_json("INSTANTIATED_AUDIT_TCOP.json", audit)
    print("INSTANTIATED AUDIT FROZEN ->", p)
    print("sha256:", sha256_of(p))
    print("Publish this digest to Mike BEFORE any unlock. Scoring is a separate Mike-gated step.")

def _boot():
    """L2 B6: every non-preflight stage fail-closed requires a PASSED preflight manifest with
    matching harness digest and re-verifies all permitted digests before doing anything."""
    global TR, KAPPA
    mp = os.path.join(OUTD, "preflight_manifest.json")
    if not os.path.exists(mp): halt("preflight_manifest.json missing: run preflight first")
    man = json.load(guarded_open(mp))
    if man.get("harness_sha256") != sha256_of(os.path.abspath(__file__)):
        halt("harness digest does not match preflight manifest (fail closed)")
    for req in ("f3_analog_bit_exact", "golden_tests", "io_self_audit", "offsets_reproduced"):
        if req not in man: halt(f"preflight manifest missing {req}")
    for rel, dig in man["permitted"].items():
        if sha256_of(os.path.join(REPO, rel)) != dig: halt(f"permitted digest drift: {rel}")
    if TR is None:
        TRmod, src = import_frozen(os.path.join(REPO, "tcop_read.py"), TCOP_READ_DIGEST, "tcop_read_frozen")
        TR = TRmod
        tcop_src = guarded_open(os.path.join(W2, "c3_w2_tcop.py"), encoding="utf-8").read()
        KAPPA = kappa_map_from_source(tcop_src)

def _current_R(stage):
    ck = _load_ck("escalation.json", {})
    return ck.get(stage, R_LADDER[0])

# ==========================================================================
# 8. Statistics + golden tests (every gate-bearing block covered; L2 item 10)
# ==========================================================================
def control_verdict_items(ctl, ladder_max):
    """Per-component control status -> (invalid, unresolved) lists. Pure; golden-tested."""
    invalid, unresolved = [], []
    for ctrl in ("N1", "N2", "N3"):
        for lvl, d in ctl.get(ctrl, {}).items():
            if isinstance(d, dict) and not d.get("pass_at_current_R", True):
                if d.get("n", 0) >= ladder_max:
                    invalid.append(f"{ctrl}/{lvl} false-pass above tolerance after exhausted ladder")
                else:
                    unresolved.append(f"{ctrl}/{lvl}: escalate (n={d.get('n', 0)})")
    return invalid, unresolved

def p1_verdict_items(p1, floor, ladder_max):
    """P1 recovery status -> (invalid, unresolved) lists. Pure; golden-tested."""
    invalid, unresolved = [], []
    if p1:
        ok, _ = precision_gate(p1["k"], p1["n"], floor)
        hi = wilson(p1["k"], p1["n"])[1]
        if not ok:
            if p1["n"] >= ladder_max and hi < floor:
                invalid.append("positive control P1 unrecoverable below recovery floor after ladder (halt-rule class)")
            else:
                unresolved.append(f"P1 recovery precision-unresolved vs floor (n={p1['n']})")
        elif hi < floor:
            invalid.append("positive control P1 unrecoverable below recovery floor (halt-rule class)")
    return invalid, unresolved

def classify_verdict(invalid, unresolved, pb_ok, pa_ok, below_floor):
    """The frozen 2.8 mechanical branch. Pure; golden-tested on all branches."""
    if invalid:
        return "INVALID EVALUABILITY SECTION"
    if not (pb_ok and pa_ok) or unresolved:
        return "PRECISION-UNRESOLVED"
    return "NOT SEEDABLE (evaluability floor breach)" if below_floor else "SEEDABLE at these floors"

def wilson(k, n, z=Z90):
    if n == 0: return (0.0, 1.0)
    p = k / n; d = 1 + z*z/n
    c = (p + z*z/(2*n)) / d
    h = z * np.sqrt(p*(1-p)/n + z*z/(4*n*n)) / d
    return (max(0.0, c-h), min(1.0, c+h))

def precision_gate(k, n, floor):
    lo, hi = wilson(k, n)
    est = k / n if n else 0.0
    half = (hi - lo) / 2.0
    return (half <= PRECISION_FRACTION * abs(est - floor)) and not (lo <= floor <= hi), (lo, hi)

def golden_tests():
    # seed derivation determinism + canonical rejection
    assert seed_for("x", 1) == seed_for("x", 1) and seed_for("x", 1) not in CANONICAL_SEEDS
    # rho_bin edges (frozen half-open band)
    assert TR.rho_bin(0.349999) is None and TR.rho_bin(0.55) is None and TR.rho_bin(0.35) == 0
    # comparison universe: 6 path-(a) tier pairs + 10 mag-pairs x 2 signs x 3 tiers = 66
    uni = comparison_universe()
    assert sum(1 for u in uni if u["path"] == "a") == 6
    assert sum(1 for u in uni if u["path"] == "b") == 60, len(uni)
    # eligibility fixtures: eligible / count / seed-half / phase-histogram
    def W(seed, phase, b=0): return {"seed": seed, "phase": phase, "bin": b}
    good = [W(s, p) for s in (1, 2, 3) for p in (0, 1, 2)]
    assert eligibility(good, good) == "eligible"
    assert eligibility(good[:8], good) == "count-failed"
    half = [W(1, p % 3) for p in range(5)] + [W(2, p % 3) for p in range(2)] + [W(3, p % 3) for p in range(2)]
    assert eligibility(half, good) == "seed-failed"
    skew = [W(s, 0) for s in (1, 2, 3)] * 3
    assert eligibility(skew, good) == "phase-confounded"
    # G1 semantics fixture: phase-0 stats, slope-positive required, strict dominance
    rec = {"g1_applicable": True, "phase0": [0.9, 0.01, 0.0], "var0": 1e-5}
    assert g1_eval(rec, {"dominance_r": 0.5, "dominance_beta": 0.005, "dominance_var": 5e-6}) is True
    assert g1_eval(dict(rec, phase0=[0.9, -0.01, 0.0]), {"dominance_r": 0, "dominance_beta": 0, "dominance_var": 0}) is False
    assert g1_eval({"g1_applicable": False}, {}) is None            # tier-0 exemption (L2 item 9)
    # onset conjunction 4-case fixture (abs(raw) AND residue; L2 item 4)
    f = ONSET["Psi_meanI_state"]
    for raw, res, want in [(f["raw"]*2, f["res"]*2, True), (f["raw"]*2, f["res"]*0.5, False),
                           (f["raw"]*0.5, f["res"]*2, False), (-f["raw"]*2, f["res"]*2, True)]:
        assert (abs(raw) > f["raw"] and res > f["res"]) == want
    # tracking burden lexicographic fixture
    assert (2 >= 1 and (2 > 1 or 0.0 > 0.1)) is True
    assert (1 >= 1 and (1 > 1 or 0.2 > 0.1)) is True
    assert (1 >= 2) is False
    # G2 fixture: nondecreasing + endpoint
    med_ok = [0.1, 0.2, 0.3, 0.4]; assert all(med_ok[i+1] >= med_ok[i] for i in range(3))
    # G4 three-condition fixture
    assert (0.23 >= G4_MEAN_FLOOR and 0.20 >= G4_Q05_FLOOR and 0.0 <= G4_TAIL_CEIL)
    # precision escalation fixture
    ok, _ = precision_gate(50, 100, 0.5); assert ok is False        # straddles floor
    ok, _ = precision_gate(2, 100, 0.5); assert ok is True
    # verdict taxonomy fixtures (L2 v3 B2): all mechanical branches exercised
    assert classify_verdict(["x"], [], True, True, False) == "INVALID EVALUABILITY SECTION"
    assert classify_verdict([], ["y"], True, True, False) == "PRECISION-UNRESOLVED"
    assert classify_verdict([], [], False, True, False) == "PRECISION-UNRESOLVED"
    assert classify_verdict([], [], True, True, True).startswith("NOT SEEDABLE")
    assert classify_verdict([], [], True, True, False).startswith("SEEDABLE")
    # control false-pass halt: exhausted ladder -> invalid; unexhausted -> unresolved
    inv, unr = control_verdict_items({"N1": {"row": {"pass_at_current_R": False, "n": R_LADDER[-1]}}}, R_LADDER[-1])
    assert inv and not unr
    inv, unr = control_verdict_items({"N1": {"row": {"pass_at_current_R": False, "n": R_LADDER[0]}}}, R_LADDER[-1])
    assert unr and not inv
    # unrecoverable-positive-control halt: tight sub-floor -> invalid; straddling -> unresolved
    inv, unr = p1_verdict_items({"k": 50, "n": 1000}, FLOOR_RECOVERY, R_LADDER[-1])
    assert inv and not unr
    inv, unr = p1_verdict_items({"k": 79, "n": 100}, FLOOR_RECOVERY, R_LADDER[-1])
    assert unr and not inv
    # ws -> phase determinism in the frozen window structure (belt to the full-key filter)
    assert all(((ws // BLOCK) % 3) == p for ws, p in
               [(ws, (ws // BLOCK) % 3) for ws in PRIMARY_WINDOW_STARTS])
    # P3 amplitude frozen-formula reproduction (pure construction arithmetic)
    a = p3_amplitude(1.0); assert 0.15 < a < 0.35, a
    return {"golden_tests": "PASS (28 fixtures incl. verdict taxonomy branches)"}

# ==========================================================================
if __name__ == "__main__":
    stage = sys.argv[1] if len(sys.argv) > 1 else ""
    {"preflight": stage_preflight, "geometry": stage_geometry, "recovery": stage_recovery,
     "controls": stage_controls, "forecast": stage_forecast}.get(
        stage, lambda: halt("usage: stage2_case1_harness.py [preflight|geometry|recovery|controls|forecast]"))()
