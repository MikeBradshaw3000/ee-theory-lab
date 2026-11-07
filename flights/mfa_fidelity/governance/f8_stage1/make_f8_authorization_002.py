"""AUTHORIZATION_002 for F8 stage 1 (the apparatus step; appends to the registry) — written on the CANONICAL machine (the stage identity carries the role and platform; only the canonical
stage can be authorized). Run from flights/mfa_fidelity/instrument in the canonical env:
    python make_f8_authorization_002.py <repo_root> <pinned_root> probe   # binds the stage (environment qualified against the pinned worktree), prints role + identities, writes NOTHING
    python make_f8_authorization_002.py <repo_root> <pinned_root> write   # also writes AUTHORIZATION_002.json and APPENDS entry 2 to the registry under governance/f8_stage1
The authorization's content is Mike's ruling (AUTHORIZED_JOBS below, issued date, issuer); every identity is measured from the bound stage."""
import os, sys, dataclasses as dc, hashlib
sys.path.insert(0, os.getcwd())
from mfa_instrument.f8 import runner as R

repo = os.path.abspath(sys.argv[1]); pinned = os.path.abspath(sys.argv[2]); mode = sys.argv[3] if len(sys.argv) > 3 else "probe"
gov = os.path.join(repo, R.GOVERNANCE_ROOT_REL)
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
def write_canon(path, obj):
    text = R._canon(R._encode(obj)); text.encode("ascii")
    with open(path, "w", newline="\n", encoding="ascii") as f: f.write(text)
    return sha(path)

# ---- Mike's ruling (2026-11-07): v2 authorizes the APPARATUS step (the prerequisite producers) and the calibration tranche; no production
VERSION = 2; ISSUED = "2026-11-07"; ISSUER = "Mike Bradshaw"
AUTHORIZED_JOBS = ("mp1_known_answer", "m6_design_audit", "m6_held_out_audit", "m6_audit_qualification",      # v1's jobs, carried (their records stay loadable under the current record)
                   "m6_price", "calibration_census", "tolerance_program", "dense_reference", "reference_stability", "projection_sweeps", "resource_benchmark")
from mfa_instrument.f8 import config as C
TRANCHE_LEVELS_MICRO = tuple(R.F8_LEVELS_MICRO[i] for i in (0, 6, 12, 18, 23))   # 0.25, 0.836957, 1.423913, 2.010870, 2.50 - spread over the pass-1 grid
TRANCHE_SEEDS = tuple(C.F8_SEED_PANEL[:3])                                           # the first three seeds of the canonical panel

st = R.bind_stage(repo, pinned)
print(f"stage role {st.role}; commit {st.commit}; platform {st.platform_tag}")
print(f"stage identity {st.result_sha256}")
print(f"governance {st.governance_sha256}; spec {st.package_spec_sha256}; adapter body {st.adapter_body_sha256}")
if st.role != "canonical":
    print("STOP: the stage is not canonical on this machine; nothing written"); sys.exit(2)
R.validate_stage_identity(st, repo, pinned); print("stage identity validates")
a = R.AuthorizationRecord(VERSION, ISSUED, ISSUER, st.result_sha256, st.governance_sha256, st.package_spec_sha256, AUTHORIZED_JOBS, True, TRANCHE_LEVELS_MICRO, TRANCHE_SEEDS, False, "")
a = dc.replace(a, result_sha256=R._digest(R._auth_body(a)))
R.validate_authorization(a, st)
rp = os.path.join(gov, R.AUTHORIZATION_REGISTRY_REL)
old = R._read_canonical(rp); R.validate_registry(old)
if old.entries[-1][0] != VERSION - 1: print(f"STOP: registry's last entry is v{old.entries[-1][0]}, expected v{VERSION-1}"); sys.exit(4)
reg = R.AuthorizationRegistry(old.entries + ((VERSION, hashlib.sha256(R._canon(R._encode(a)).encode("ascii")).hexdigest()),))
reg = dc.replace(reg, result_sha256=R._digest(reg.entries)); R.validate_registry(reg)
print(f"authorization v{VERSION} result {a.result_sha256}; jobs {AUTHORIZED_JOBS}; tranche True levels {TRANCHE_LEVELS_MICRO} seeds {TRANCHE_SEEDS}; production False")
print(f"AUTHORIZATION_{VERSION:03d}.json would be {reg.entries[-1][1]}; registry entries {reg.entries}; registry result {reg.result_sha256}")
if mode != "write": print("probe only; nothing written"); sys.exit(0)
ap = os.path.join(gov, f"AUTHORIZATION_{VERSION:03d}.json")
if os.path.exists(ap): print("STOP: AUTHORIZATION_%03d.json already exists; each authorization gets exactly one commit" % VERSION); sys.exit(3)
fa = write_canon(ap, a); fr = write_canon(rp, reg)
assert fa == reg.entries[-1][1]
print(f"written AUTHORIZATION_{VERSION:03d}.json {fa}; AUTHORIZATION_REGISTRY.json {fr}")
