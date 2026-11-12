"""F8 M6 job-0 comparison supplement (generator declaration v0.3 s8; ratified M6-10; Interpretation 002 pt 9b). DESCRIPTIVE ONLY.
Run from flights/mfa_fidelity/instrument:   python make_f8_job0_comparison.py <repo_root> <out_json>
Lattice side: the committed canonical calibration census (job 0), realization object, 20 calibration seeds per pass-1 level - tail density per
Interpretation 001 as the census records it (rho_hat_re). Surrogate side: M6's placed surrogate_level_stats - unmodulated E, n_cmp = 200 runs per
level, stream SeedSequence([pricing_master, 1, level_micro, replicate]). No lattice run, no canonical job, no M7 record; nothing here is scored,
retunes the generator, or bears on P1. Signed differences are lattice minus surrogate. Writes one canonical-JSON file and prints its identity."""
import os, sys, json, math, hashlib, platform, statistics as st
sys.path.insert(0, os.getcwd())
import numpy as np
from mfa_instrument.f8 import runner as R, audit as A, closure as CL

repo = os.path.abspath(sys.argv[1]); out = sys.argv[2]
cpath = os.path.join(repo, R.GOVERNANCE_ROOT_REL, R.PREREQUISITES_REL, "package", "calibration_census.json")
def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
env = json.load(open(cpath, encoding="ascii")); census = R._decode(env["record"])
assert type(census).__name__ == "CalibrationCensus" and census.role == "canonical" and env["job"] == "calibration_census"
A.verify_frozen_identity()
master = A.production_masters()[2]; n_cmp = A.COMPARISON_REPLICATES
assert n_cmp == 200 and tuple(census.levels_micro) == tuple(A.F8_LEVELS_MICRO)
rows = []
for i, u in enumerate(census.levels_micro):
    lat = [float(x) for x in census.rho_hat_re[i]]; n = len(lat); assert n == 20
    lm = sum(lat) / n; ls = st.stdev(lat)                      # ddof = 1
    assert abs(ls - census.s_hat_re[i]) <= 1e-15, (u, ls, census.s_hat_re[i])   # the census's own s_hat is this SD
    s = A.surrogate_level_stats(int(u), master, n_cmp)
    rows.append({"level_micro": int(u), "m": CL.level_m(int(u)),
                 "lattice_tail_mean": lm, "surrogate_tail_mean": s.tail_mean, "mean_difference_lattice_minus_surrogate": lm - s.tail_mean,
                 "lattice_s_hat": ls, "surrogate_sd": s.tail_sd, "sd_difference_lattice_minus_surrogate": ls - s.tail_sd,
                 "sd_ratio_surrogate_over_lattice": (s.tail_sd / ls) if ls > 0.0 else "undefined",
                 "lattice_se_mean": ls / math.sqrt(n), "lattice_se_sd_approx": ls / math.sqrt(2 * (n - 1)),
                 "surrogate_se_mean": s.se_mean, "surrogate_se_sd_approx": s.se_sd_approx})
body = {"title": "F8 M6 job-0 comparison supplement (descriptive)",
        "authority": "generator declaration v0.3 s8; ratification record v1.0 M6-10; F8 Interpretation 002 pt 9b",
        "census_file_sha256": sha(cpath), "census_result_sha256": census.result_sha256, "calibration_master": int(census.calibration_master),
        "lattice_object": "realization", "lattice_seeds_per_level": 20, "lattice_observable": "rho_hat: mean over the 1,000-tick tail (Interpretation 001), as recorded in the census",
        "surrogate": "unmodulated E (M6 gen_sustained_run), surrogate_level_stats", "surrogate_replicates_per_level": int(n_cmp), "pricing_master": int(master),
        "surrogate_stream": "SeedSequence([pricing_master, 1, level_micro, replicate])",
        "generator_declaration_sha256": A.GENERATOR_DECLARATION_SHA256_LITERAL, "audit_source_sha256": sha(A.__file__), "runner_source_sha256": sha(R.__file__),
        "sign_convention": "differences are lattice minus surrogate; the SD ratio is surrogate over lattice",
        "se_convention": "se_mean = sd/sqrt(n); se_sd_approx = sd/sqrt(2(n-1))",
        "levels": rows, "insertion_levels": "not covered",
        "statement": "The E surrogate has no spatial dependence. The lattice/closure amplitude mismatch is the fidelity tier's object (contract s1.2', Appendix B.4). This supplement is descriptive: it is not a prerequisite for the M6 audits, never retunes the generator, makes no claim that surrogate variance bounds lattice variance, and does not transfer the M6 synthetic-ensemble error rates to lattice runs.",
        "platform": f"{platform.system()}-{platform.machine()}-py{platform.python_version()}-np{np.__version__}"}
ident = hashlib.sha256(json.dumps(body, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("ascii")).hexdigest()
doc = dict(body); doc["result_sha256"] = ident
text = json.dumps(doc, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n"; text.encode("ascii")
with open(out, "w", newline="\n", encoding="ascii") as f: f.write(text)
print(f"written {out} sha256 {sha(out)}; result_sha256 {ident}; platform {body['platform']}")
print(f"{'m':>9} {'lat mean':>9} {'sur mean':>9} {'diff':>9} {'lat s':>8} {'sur sd':>8} {'ratio':>6}")
for r in rows: print(f"{r['m']:9.6f} {r['lattice_tail_mean']:9.5f} {r['surrogate_tail_mean']:9.5f} {r['mean_difference_lattice_minus_surrogate']:+9.5f} {r['lattice_s_hat']:8.5f} {r['surrogate_sd']:8.5f} {r['sd_ratio_surrogate_over_lattice']:6.2f}")
