"""AUTHORIZATION_001 for F8 stage 1 — written on the CANONICAL machine (the stage identity carries the role and platform; only the canonical
stage can be authorized). Run from flights/mfa_fidelity/instrument in the canonical env:
    python make_f8_authorization_001.py <repo_root> <pinned_root> probe   # binds the stage (environment qualified against the pinned worktree), prints role + identities, writes NOTHING
    python make_f8_authorization_001.py <repo_root> <pinned_root> write   # also writes AUTHORIZATION_001.json and the registry (first entry) under governance/f8_stage1
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

# ---- Mike's ruling (2026-11-05): v1 authorizes the s7.1 QUALIFICATION step only; no tranche, no production
VERSION = 1; ISSUED = "2026-11-05"; ISSUER = "Mike Bradshaw"
AUTHORIZED_JOBS = ("mp1_known_answer", "m6_design_audit", "m6_held_out_audit", "m6_audit_qualification")

st = R.bind_stage(repo, pinned)
print(f"stage role {st.role}; commit {st.commit}; platform {st.platform_tag}")
print(f"stage identity {st.result_sha256}")
print(f"governance {st.governance_sha256}; spec {st.package_spec_sha256}; adapter body {st.adapter_body_sha256}")
if st.role != "canonical":
    print("STOP: the stage is not canonical on this machine; nothing written"); sys.exit(2)
R.validate_stage_identity(st, repo, pinned); print("stage identity validates")
a = R.AuthorizationRecord(VERSION, ISSUED, ISSUER, st.result_sha256, st.governance_sha256, st.package_spec_sha256, AUTHORIZED_JOBS, False, (), (), False, "")
a = dc.replace(a, result_sha256=R._digest(R._auth_body(a)))
R.validate_authorization(a, st)
reg = R.AuthorizationRegistry(((VERSION, hashlib.sha256(R._canon(R._encode(a)).encode("ascii")).hexdigest()),))
reg = dc.replace(reg, result_sha256=R._digest(reg.entries)); R.validate_registry(reg)
print(f"authorization v{VERSION} result {a.result_sha256}; jobs {AUTHORIZED_JOBS}; tranche False; production False")
print(f"AUTHORIZATION_{VERSION:03d}.json would be {reg.entries[0][1]}; registry result {reg.result_sha256}")
if mode != "write": print("probe only; nothing written"); sys.exit(0)
ap = os.path.join(gov, f"AUTHORIZATION_{VERSION:03d}.json"); rp = os.path.join(gov, R.AUTHORIZATION_REGISTRY_REL)
if os.path.exists(ap) or os.path.exists(rp): print("STOP: an authorization or registry file already exists; each gets exactly one commit"); sys.exit(3)
fa = write_canon(ap, a); fr = write_canon(rp, reg)
assert fa == reg.entries[0][1]
print(f"written AUTHORIZATION_{VERSION:03d}.json {fa}; AUTHORIZATION_REGISTRY.json {fr}")
