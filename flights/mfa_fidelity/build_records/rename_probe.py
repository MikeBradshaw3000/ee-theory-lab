"""Probe: does os.replace(dir.partial -> dir) fail on this machine right after writing parquet + json files into it?
Mimics mfa_instrument.f8.runner.run_level's persistence (20 runs: write_rho_table + a json) with no instrument code.
Reports per-trial outcome and, on failure, whether a retry with backoff succeeds and after how long."""
import os, sys, time, json, tempfile, platform, hashlib
import numpy as np, pyarrow as pa, pyarrow.parquet as pq

base = tempfile.mkdtemp(prefix="rename_probe_")
trials, fails, retried_ok, lines = 60, 0, 0, []
for t in range(trials):
    level = os.path.join(base, f"level{t}"); partial = level + ".partial"
    os.makedirs(partial)
    for seed in range(20):
        rho = np.random.default_rng(seed).random(4000)
        p = os.path.join(partial, f"run_{seed}.parquet")
        pq.write_table(pa.table({"Tick": pa.array(np.arange(len(rho), dtype=np.int64)), "rho_global": pa.array(rho, type=pa.float64())}), p)
        h = hashlib.sha256(open(p, "rb").read()).hexdigest()
        with open(os.path.join(partial, f"run_{seed}.json"), "w", newline="\n", encoding="utf-8") as f: f.write(json.dumps({"seed": seed, "rho": h}))
    t0 = time.perf_counter()
    try:
        os.replace(partial, level); lines.append(f"trial {t}: ok")
    except PermissionError as e:
        fails += 1; ok = False
        for k in range(50):
            time.sleep(0.1)
            try: os.replace(partial, level); ok = True; break
            except PermissionError: pass
        dt = time.perf_counter() - t0
        if ok: retried_ok += 1
        lines.append(f"trial {t}: PermissionError ({e.winerror}); retry {'succeeded' if ok else 'FAILED'} after {dt:.2f}s")
out = [f"platform {platform.platform()} py{platform.python_version()} np{np.__version__} pyarrow{pa.__version__}", f"base {base}",
       f"trials {trials}: failures {fails}, of which recovered by retry {retried_ok}"] + [l for l in lines if "Permission" in l]
print("\n".join(out))
