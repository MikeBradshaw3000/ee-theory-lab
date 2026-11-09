"""Production prerequisite manifest for F8 stage 1 — written on the CANONICAL machine from COMMITTED records (run from flights/mfa_fidelity/instrument):
    python make_f8_prereq_manifest.py <repo_root> <pinned_root> probe   # loads every prerequisite record through M7's reader, prints the entries, writes nothing
    python make_f8_prereq_manifest.py <repo_root> <pinned_root> write   # also writes governance/f8_stage1/PRODUCTION_PREREQUISITE_MANIFEST.json (canonical ASCII)
The entry set is the governance record's seven production prerequisites (G4); each entry carries the committed file's identity and the record identity M7 computes
(load_record with the entry's own context: type, producing job, dependencies). The manifest validator refuses any entry that does not load, so a wrong manifest cannot be written."""
import os, sys, dataclasses as dc, hashlib
sys.path.insert(0, os.getcwd())
from mfa_instrument.f8 import runner as R

repo = os.path.abspath(sys.argv[1]); pinned = os.path.abspath(sys.argv[2]); mode = sys.argv[3] if len(sys.argv) > 3 else "probe"
gov = os.path.join(repo, R.GOVERNANCE_ROOT_REL); base = os.path.join(gov, R.PREREQUISITES_REL)
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()

st = R.bind_stage(repo, pinned)
print(f"stage role {st.role}; commit {st.commit}; identity {st.result_sha256}", flush=True)
if st.role != "canonical": print("STOP: stage not canonical"); sys.exit(2)
g, gsha = R.load_governance(repo, st)
print(f"governance {gsha}; prerequisites {[p[0] for p in g.production_prerequisites]}")
FILES = {"calibration_tranche": "calibration_tranche.json", "resource_actuals": "package/resource_benchmark.json", "mp1_known_answer": "package/mp1_known_answer.json",
         "m6_audit_qualification": "package/m6_audit_qualification.json", "calibration_census": "package/calibration_census.json",
         "dense_reference": "package/dense_reference.json", "reference_stability": "package/reference_stability.json"}
DEPS = {"m6_audit_qualification": (("design", "package/m6_design_audit.json"), ("held_out", "package/m6_held_out_audit.json")),
        "reference_stability": (("primary", "package/dense_reference.json"),)}
def entry(name):
    rel = FILES[name]; fp = os.path.join(base, *rel.split("/"))
    deps = tuple((role, drel, sha(os.path.join(base, *drel.split("/")))) for role, drel in DEPS.get(name, ()))
    probe = R.PrerequisiteEntry(name, R.PREREQ_TYPES[name], rel, sha(fp), "0" * 64, deps)
    rec = R.load_record(fp, R.PREREQ_TYPES[name], st, repo, pinned, require_job=R.PREREQ_JOBS[name], **R._prereq_context(probe, base, st, repo, pinned, fp))[0]
    e = R.PrerequisiteEntry(name, R.PREREQ_TYPES[name], rel, sha(fp), R._item_identity(rec), deps)
    print(f"  {name:24s} {e.record_type:26s} {rel:36s} file {e.file_sha256[:16]} identity {e.record_identity[:16]} deps {[d[0] for d in deps]}")
    return e
entries = tuple(entry(p[0]) for p in g.production_prerequisites)
man = R.ProductionPrerequisiteManifest(gsha, entries); man = dc.replace(man, result_sha256=R._digest(R._manifest_body(man)))
R.validate_prerequisite_manifest(man)
if set(e.name for e in man.entries) != set(p[0] for p in g.production_prerequisites) or man.governance_sha256 != gsha: print("STOP: manifest set differs from the governance record"); sys.exit(5)
text = R._canon(R._encode(man)); text.encode("ascii")
print(f"manifest result {man.result_sha256}; file would be {hashlib.sha256(text.encode('ascii')).hexdigest()}")
if mode != "write": print("probe only; nothing written"); sys.exit(0)
mp = os.path.join(gov, R.PREREQ_MANIFEST_REL)
if os.path.exists(mp): print("STOP: manifest already exists"); sys.exit(3)
with open(mp, "w", newline="\n", encoding="ascii") as f: f.write(text)
print(f"written {R.PREREQ_MANIFEST_REL} {sha(mp)}")
