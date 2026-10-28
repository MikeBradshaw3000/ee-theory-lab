"""run_f8_m3_validation_attempt2.py — execute the RATIFIED attempt-2 null-validation protocol (Mike, 2026-10-27) on the
canonical machine and write the record. Refuses to run unless null.py is the identity this protocol was ratified with.
Usage (from flights/mfa_fidelity/instrument, canonical venv): python run_f8_m3_validation_attempt2.py <out_json>
"""
import dataclasses, hashlib, json, os, platform, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
NULL_PY_SHA256 = "4ee3f239b27f772b64a3f31a6dfff73112c40386904e3bda50e826766cef0121"

def main(out_path: str) -> int:
    null_path = os.path.join(HERE, "mfa_instrument", "f8", "null.py")
    sha = hashlib.sha256(open(null_path, "rb").read()).hexdigest()
    if sha != NULL_PY_SHA256:
        print(f"REFUSED: null.py identity {sha[:16]} is not the ratified {NULL_PY_SHA256[:16]}"); return 2
    import numpy, mfa_instrument.f8.null as N
    P = N.VALIDATION_PROTOCOL_ATTEMPT_2
    N.verify_protocol_registration(P)
    t0 = time.time()
    v = N.validate_on_stepper(P.n_replicates, P.replicate_master, grid=P.grid, ticks=P.ticks, protocol=P)
    elapsed = time.time() - t0
    rec = {"__type__": "F8NullValidationAttempt", "attempt": 2, "status": "PASSED" if v.qualification_passed else "FAILED",
           "protocol_id": P.protocol_id, "protocol_sha256": P.identity(), "null_py_sha256": sha, "elapsed_s": round(elapsed, 1),
           "environment": {"python": sys.version.split()[0], "numpy": numpy.__version__, "platform": platform.platform(), "node": platform.node()},
           "primary_bound": P.primary_bound(), "auxiliary_bound": P.auxiliary_bound(), "record": dataclasses.asdict(v)}
    js = json.dumps(rec, sort_keys=True, separators=(",", ":"), allow_nan=False)
    with open(out_path, "w", newline="\n") as f: f.write(js + "\n")
    h = hashlib.sha256(open(out_path, "rb").read()).hexdigest()
    print(f"attempt 2 {rec['status']}: designated {v.dkw_sup_deviation:.4f} vs {P.primary_bound():.4f}; union max {max(v.per_window_sup_deviation):.4f} vs {P.auxiliary_bound():.4f}; "
          f"mean {v.empirical_mean_density:.6f} sd {v.empirical_sd_density:.7f}; S_min>theta_P {v.s_min_rejection_rate}; {elapsed:.0f}s")
    print(f"record sha256 {h}")
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "f8_m3_null_validation_attempt2.json"))
