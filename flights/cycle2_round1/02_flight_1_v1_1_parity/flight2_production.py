"""
Cycle 2 Round 1 Flight 2 production substrate.
Patched from Gemini's flight2_production.py with two memory-management changes:

  1. Streaming parquet writes: telemetry written to disk every CHUNK_TICKS ticks
     and the in-memory accumulator cleared. Peak memory bounded by chunk size,
     not by total run size.

  2. Per-run command-line dispatch: invoke as
       python flight2_production.py --run probe1_20x20
     to run a single production file. Memory from prior runs cannot accumulate.
     Running without --run executes all four production runs sequentially
     (original orchestrator behavior, less safe at 40x40 on 16 GB RAM).

Substrate logic unchanged from architectural review: same F-form selection,
same tick semantics, same Section 15 prohibition compliance. All five Flight 1
deferred remediations preserved.

Memory diagnostics added: peak resident memory printed after each run.
"""
import sys
import os
import time
import shutil
import gc
import argparse
from pathlib import Path
import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

# --- PATH DISCIPLINE ---
SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR / "flight2_outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

# --- DECLARATION PER V1.1 SECTION 4 ---
# "NumPy substrate implementation of locked Mesa-equivalent dynamics."
# Note: As Mesa 3.x API regressions and extreme performance degradation blocked physical execution,
# this pure NumPy implementation is established as the canonical baseline substrate.

# --- SECTION 3: GLOBAL PARAMETERS ---
PRNG_SEED = 0x7A9B31C
TICKS_PRODUCTION = 3000
ALPHA = 4.0
BETA = 3.0
DELTA = 4.0
GAMMA_OFFSET = 4.0
ETA = 0.01
GAMMA_Q = 0.001
W_V = 0.33
W_U = 0.33
W_R = 0.34
BASE_INIT_LOW = 0.6
BASE_INIT_HIGH = 0.9

# --- MEMORY MANAGEMENT ---
# Chunked write: flush telemetry to disk every CHUNK_TICKS ticks.
# At 40x40 (1600 cells), CHUNK_TICKS=500 holds 800k rows in memory at a time
# (peak ~1 GB during write), vs 4.8M rows / ~6 GB at full-run accumulation.
CHUNK_TICKS = 500


# === ENVIRONMENT VERIFICATION ===

def verify_environment():
    print("--- LAUNCH: SESSION RESILIENCE VERIFICATION ---")
    if sys.prefix == sys.base_prefix:
        raise RuntimeError(
            f"Venv not activated. sys.prefix is {sys.prefix}. "
            "Run '.\\venv\\Scripts\\Activate.ps1' from the project root and retry."
        )
    if sys.version_info[:2] != (3, 14):
        raise RuntimeError(
            f"Wrong Python version: {sys.version}. Expected 3.14.x. "
            "The venv may not be activated, or the venv's Python doesn't match."
        )

    print(f"[env] Python {sys.version_info[0]}.{sys.version_info[1]}.{sys.version_info[2]} OK")
    print(f"[env] numpy {np.__version__}, pandas {pd.__version__}, pyarrow {pa.__version__}")
    print(f"[env] Working directory: {os.getcwd()}")
    print(f"[env] Script directory: {SCRIPT_DIR}")
    print(f"[env] Output directory: {OUTPUT_DIR}")
    print(f"[env] Chunk ticks: {CHUNK_TICKS}")
    print("--- ENV VERIFIED. PROCEEDING TO FLIGHT 2 ---")


def get_peak_memory_mb():
    """Return peak resident memory in MB. Cross-platform fallback to current memory if peak unavailable."""
    try:
        # Windows: use psutil if available
        import psutil
        proc = psutil.Process()
        return proc.memory_info().rss / (1024 * 1024)
    except ImportError:
        # Fallback: report current Python heap size approximately
        import resource
        try:
            return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024
        except Exception:
            return -1.0  # unavailable


# === SUBSTRATE ===

def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))


class NumpyEEModel:
    def __init__(self, grid_scale, f_form):
        self.grid_scale = grid_scale
        self.f_form = f_form
        self.prng = np.random.default_rng(PRNG_SEED)

        self.v = np.zeros(self.grid_scale, dtype=np.float64)
        self.u = np.zeros(self.grid_scale, dtype=np.float64)
        self.r = np.zeros(self.grid_scale, dtype=np.float64)
        self.is_active = np.zeros(self.grid_scale, dtype=bool)

        # Section 5.2: sequence preservation via cell-by-cell PRNG draws
        for x in range(self.grid_scale[0]):
            for y in range(self.grid_scale[1]):
                self.v[x, y] = self.prng.uniform(BASE_INIT_LOW, BASE_INIT_HIGH)
                self.u[x, y] = self.prng.uniform(BASE_INIT_LOW, BASE_INIT_HIGH)
                self.r[x, y] = self.prng.uniform(BASE_INIT_LOW, BASE_INIT_HIGH)
                self.is_active[x, y] = self.prng.random() < 0.5

        self.tick_count = 0
        self.clipped_v_count = 0
        self.clipped_u_count = 0
        self.clipped_r_count = 0

        self.telemetry_buffer = []  # cleared per chunk
        self.moore_offsets = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    def get_moore_sum(self, grid_matrix):
        total = np.zeros_like(grid_matrix, dtype=np.float64)
        for dx, dy in self.moore_offsets:
            total += np.roll(np.roll(grid_matrix, dx, axis=0), dy, axis=1)
        return total

    def step(self):
        tick_idx = self.tick_count

        # Step 1: Read pre-Q bases
        b_i_v = self.v.copy()
        b_i_u = self.u.copy()
        b_i_r = self.r.copy()

        bases_stack = np.stack([self.v, self.u, self.r], axis=0)
        limiting_base_argmin = np.argmin(bases_stack, axis=0)
        lambda_multiplicative = self.v * self.u * self.r
        lambda_additive = W_V * self.v + W_U * self.u + W_R * self.r

        # Step 2: Compute Lambda (F-form selection)
        if self.f_form == "F_baseline":
            lambda_total = (self.v + self.u + self.r) / 3.0
        elif self.f_form == "F_LR":
            lambda_total = np.min(bases_stack, axis=0)
        elif self.f_form == "F_2_symmetric":
            lambda_total = lambda_multiplicative * lambda_additive
        else:
            raise ValueError(f"Unknown F-form: {self.f_form}")

        # Step 3: Compute local density
        active_int = self.is_active.astype(np.float64)
        local_density = self.get_moore_sum(active_int) / 8.0

        # Step 4: Compute drive components
        term_lambda = ALPHA * lambda_total
        term_density_pos = BETA * local_density
        term_overcrowding = -DELTA * (local_density ** 2)
        term_offset = np.full_like(self.v, -GAMMA_OFFSET)
        drive_raw = term_lambda + term_density_pos + term_overcrowding + term_offset

        # Step 5: Compute probability chain
        p_base = sigmoid(drive_raw)
        p_act = np.clip(p_base + ETA * (1.0 - p_base), 0.0, 1.0)

        # Step 6: Draw and determine next state
        prng_draw = self.prng.random(size=self.grid_scale)
        next_state = prng_draw < p_act

        # Step 7 & 8: Synchronous advance and activation change
        ds = next_state.astype(int) - self.is_active.astype(int)
        self.is_active = next_state.copy()

        # Step 9: Compute Psi_local
        sum_neighbor_ds = self.get_moore_sum(ds.astype(np.float64))
        psi_local = ds * sum_neighbor_ds

        # Step 11: Apply Q operator (committed arbitration: local Ψ_local input)
        delta_v = GAMMA_Q * psi_local
        delta_u = GAMMA_Q * psi_local
        delta_r = GAMMA_Q * psi_local

        # Step 13: Record telemetry to buffer
        xs, ys = np.indices(self.grid_scale)
        xs = xs.flatten()
        ys = ys.flatten()

        for i in range(len(xs)):
            x, y = xs[i], ys[i]
            row = {
                "Tick": tick_idx,
                "Agent_X": x,
                "Agent_Y": y,
                "b_i_v": b_i_v[x, y],
                "b_i_u": b_i_u[x, y],
                "b_i_r": b_i_r[x, y],
                "limiting_base_argmin": limiting_base_argmin[x, y],
                "Lambda_multiplicative": lambda_multiplicative[x, y],
                "Lambda_additive": lambda_additive[x, y],
                "Lambda_total": lambda_total[x, y],
                "Local_Density": local_density[x, y],
                "Drive_Raw": drive_raw[x, y],
                "Term_Density_Pos": term_density_pos[x, y],
                "Term_Overcrowding": term_overcrowding[x, y],
                "Term_Offset": term_offset[x, y],
                "p_base": p_base[x, y],
                "p_act": p_act[x, y],
                "PRNG_draw": prng_draw[x, y],
                "is_active": self.is_active[x, y],
                "Psi_local": psi_local[x, y],
                "gamma_coef": GAMMA_Q,
                "Delta_v": delta_v[x, y],
                "Delta_u": delta_u[x, y],
                "Delta_r": delta_r[x, y],
                "Term_Lambda": term_lambda[x, y]
            }
            self.telemetry_buffer.append(row)

        # Step 12: Update bases with clipping tracking
        v_new = self.v + delta_v
        u_new = self.u + delta_u
        r_new = self.r + delta_r

        clipped_v_mask = (v_new < 0.0) | (v_new > 1.0)
        clipped_u_mask = (u_new < 0.0) | (u_new > 1.0)
        clipped_r_mask = (r_new < 0.0) | (r_new > 1.0)

        self.clipped_v_count += int(np.sum(clipped_v_mask))
        self.clipped_u_count += int(np.sum(clipped_u_mask))
        self.clipped_r_count += int(np.sum(clipped_r_mask))

        self.v = np.clip(v_new, 0.0, 1.0)
        self.u = np.clip(u_new, 0.0, 1.0)
        self.r = np.clip(r_new, 0.0, 1.0)

        self.tick_count += 1

    def flush_buffer_to_writer(self, writer):
        """Convert telemetry_buffer to a pyarrow Table and append to writer.
        Clears the buffer afterward."""
        if not self.telemetry_buffer:
            return 0
        df = pd.DataFrame(self.telemetry_buffer)
        table = pa.Table.from_pandas(df, preserve_index=False)
        writer.write_table(table)
        rows_flushed = len(df)
        # Aggressive cleanup
        self.telemetry_buffer.clear()
        del df
        del table
        return rows_flushed


# === POST-EXECUTION VERIFICATION ===

def post_execution_verification(filepath, expected_rows, expected_columns, model):
    print(f"\n--- Post-Execution Verification: {filepath.name} ---")
    if not filepath.exists():
        print(f"ERROR: Target file not found at {filepath}")
        return False

    file_size_bytes = os.path.getsize(filepath)

    # Read parquet for verification. Read in batches if file is large to bound memory.
    pf = pq.ParquetFile(filepath)
    total_rows = pf.metadata.num_rows
    actual_cols = pf.metadata.num_columns

    # Realization Invariant Check: streamed across batches
    invariant_mismatches = 0
    tick_min = None
    tick_max = None
    unique_cells = set()

    for batch in pf.iter_batches(batch_size=200000, columns=['Tick', 'Agent_X', 'Agent_Y',
                                                              'is_active', 'PRNG_draw', 'p_act']):
        df_batch = batch.to_pandas()
        # Realization invariant on this batch
        invariant_mask = df_batch['is_active'] == (df_batch['PRNG_draw'] < df_batch['p_act'])
        invariant_mismatches += int((~invariant_mask).sum())
        # Tick range
        t_min = df_batch['Tick'].min()
        t_max = df_batch['Tick'].max()
        tick_min = t_min if tick_min is None else min(tick_min, t_min)
        tick_max = t_max if tick_max is None else max(tick_max, t_max)
        # Unique cells
        for x, y in zip(df_batch['Agent_X'].values, df_batch['Agent_Y'].values):
            unique_cells.add((int(x), int(y)))
        del df_batch

    shape_pass = (total_rows == expected_rows) and (actual_cols == expected_columns)
    invariant_pass = (invariant_mismatches == 0)

    print(f"File size: {file_size_bytes:,} bytes")
    print(f"Row count: {total_rows:,} (expected {expected_rows:,})")
    print(f"Column count: {actual_cols} (expected {expected_columns})")
    print(f"Required 25 columns present: {actual_cols >= 25}")
    print(f"Tick range: {tick_min} to {tick_max} (expected 0 to {TICKS_PRODUCTION - 1})")
    print(f"Unique cells: {len(unique_cells)} (expected {expected_rows // TICKS_PRODUCTION})")
    print(f"F_variant: {model.f_form}")
    print(f"Non-empty: {total_rows > 0}")
    print(f"Realization invariant satisfied: {invariant_pass} ({invariant_mismatches:,} mismatches across all {total_rows:,} rows)")
    print(f"Clipping summary: v={model.clipped_v_count}, u={model.clipped_u_count}, r={model.clipped_r_count}")

    if shape_pass and invariant_pass:
        print("ARTIFACT VERIFIED")
        return True
    else:
        print("ARTIFACT FAILED VERIFICATION")
        return False


# === RUN ORCHESTRATION ===

def run_simulation(grid_scale, f_form, base_filename):
    """Execute one production run with streaming parquet writes.
    Returns (filepath, verification_success)."""
    print(f"\nInitializing Run: {f_form} at {grid_scale[0]}x{grid_scale[1]} for {TICKS_PRODUCTION} ticks...")
    print(f"  (chunked writes every {CHUNK_TICKS} ticks)")
    start_time = time.time()

    model = NumpyEEModel(grid_scale=grid_scale, f_form=f_form)
    filepath = OUTPUT_DIR / base_filename

    # Build pyarrow schema from a single-row sample to initialize the writer
    # Run tick 0 first to get the buffer populated, then extract schema
    model.step()
    if not model.telemetry_buffer:
        raise RuntimeError("Telemetry buffer empty after first tick — substrate broken")

    sample_df = pd.DataFrame(model.telemetry_buffer[:1])
    sample_table = pa.Table.from_pandas(sample_df, preserve_index=False)
    schema = sample_table.schema

    # Attach metadata per v1.1 Section 13.4
    custom_metadata = {
        b"F_variant": str(f_form).encode(),
        b"Scale": str(grid_scale[0]).encode(),
        b"PRNG_seed": str(PRNG_SEED).encode(),
        b"Substrate_version": b"v1.1",
        b"Total_ticks": str(TICKS_PRODUCTION).encode(),
        b"Execution_timestamp": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()).encode()
    }
    existing_meta = schema.metadata or {}
    merged_meta = {**existing_meta, **custom_metadata}
    schema = schema.with_metadata(merged_meta)

    del sample_df
    del sample_table

    rows_written = 0
    with pq.ParquetWriter(filepath, schema, compression='snappy') as writer:
        # Flush tick 0 (already computed) into the writer using schema-aware path
        # First flush uses schema-derived table, subsequent flushes use the same schema
        first_chunk_df = pd.DataFrame(model.telemetry_buffer)
        first_chunk_table = pa.Table.from_pandas(first_chunk_df, preserve_index=False, schema=schema)
        writer.write_table(first_chunk_table)
        rows_written += len(first_chunk_df)
        model.telemetry_buffer.clear()
        del first_chunk_df
        del first_chunk_table

        # Continue from tick 1 to TICKS_PRODUCTION-1, flushing every CHUNK_TICKS
        for tick in range(1, TICKS_PRODUCTION):
            model.step()
            # Flush at chunk boundary or final tick
            if model.tick_count % CHUNK_TICKS == 0 or model.tick_count == TICKS_PRODUCTION:
                df_chunk = pd.DataFrame(model.telemetry_buffer)
                table_chunk = pa.Table.from_pandas(df_chunk, preserve_index=False, schema=schema)
                writer.write_table(table_chunk)
                rows_written += len(df_chunk)
                model.telemetry_buffer.clear()
                del df_chunk
                del table_chunk
                gc.collect()

    execution_time = time.time() - start_time
    peak_mb = get_peak_memory_mb()
    print(f"Execution complete in {execution_time:.2f} seconds.")
    print(f"Rows written to parquet: {rows_written:,}")
    if peak_mb > 0:
        print(f"Peak resident memory: {peak_mb:,.1f} MB")

    expected_rows = grid_scale[0] * grid_scale[1] * TICKS_PRODUCTION
    verification_success = post_execution_verification(filepath, expected_rows, 25, model)

    # Cleanup before next run
    del model
    gc.collect()

    return filepath, verification_success


# === SHADOW COPIES ===

def make_shadow_copies(source_path, shadow_filenames):
    """Make byte-identical shadow copies of the F_2_symmetric source for the
    probe1/probe2-F2sym/probe3 trio per v1.1 Section 13.2."""
    print(f"\nCreating shadow copies of {source_path.name}...")
    for shadow_filename in shadow_filenames:
        shadow_path = OUTPUT_DIR / shadow_filename
        shutil.copy2(source_path, shadow_path)
        size = os.path.getsize(shadow_path)
        print(f"  copied to {shadow_filename} ({size:,} bytes)")
    print("Shadow copies created.")


# === RUN DEFINITIONS ===

# Each entry: (run_key, grid_scale, f_form, base_filename, shadow_filenames_or_None)
RUNS = {
    "probe1_20x20": ((20, 20), "F_2_symmetric", "flight6_probe1_overcrowding_20x20.parquet",
                     ["flight6_probe2_starvation_F2sym_20x20.parquet",
                      "flight6_probe3_fusion_residual_20x20.parquet"]),
    "flr_20x20":    ((20, 20), "F_LR", "flight6_probe2_starvation_FLR_20x20.parquet", None),
    "probe1_40x40": ((40, 40), "F_2_symmetric", "flight6_probe1_overcrowding_40x40.parquet",
                     ["flight6_probe2_starvation_F2sym_40x40.parquet",
                      "flight6_probe3_fusion_residual_40x40.parquet"]),
    "flr_40x40":    ((40, 40), "F_LR", "flight6_probe2_starvation_FLR_40x40.parquet", None),
}


def execute_run(run_key):
    """Execute a single run by key. Returns True if it passed verification."""
    if run_key not in RUNS:
        raise ValueError(f"Unknown run key: {run_key}. Valid keys: {list(RUNS.keys())}")
    grid_scale, f_form, base_filename, shadow_filenames = RUNS[run_key]
    filepath, passed = run_simulation(grid_scale, f_form, base_filename)
    if passed and shadow_filenames:
        make_shadow_copies(filepath, shadow_filenames)
    return passed


def execute_all_runs():
    """Sequential execution of all four production runs.
    Less safe at 40×40 on 16 GB RAM due to accumulated memory; prefer per-run invocation."""
    all_passed = True
    for run_key in ["probe1_20x20", "flr_20x20", "probe1_40x40", "flr_40x40"]:
        passed = execute_run(run_key)
        all_passed = all_passed and passed
        gc.collect()

    print("\n--- FINAL FLIGHT 2 VERIFICATION SUMMARY ---")
    if all_passed:
        print("ALL ARTIFACTS PRESENT AND VERIFIED")
    else:
        print("FLIGHT 2 FAILED: ONE OR MORE ARTIFACTS DID NOT PASS VERIFICATION")
    return all_passed


# === ENTRY POINT ===

def main():
    parser = argparse.ArgumentParser(
        description="Flight 2 production substrate. Run one production file at a time (recommended) or all four sequentially."
    )
    parser.add_argument(
        "--run",
        type=str,
        default=None,
        help=f"Single run to execute. One of: {', '.join(RUNS.keys())}. Omit to run all four sequentially."
    )
    args = parser.parse_args()

    import warnings
    warnings.filterwarnings("ignore", category=FutureWarning, module="pandas")

    verify_environment()

    if args.run is None:
        print("\nNo --run specified; executing all four production runs sequentially.")
        print("WARNING: On a 16 GB system, prefer per-run invocation (--run KEY).")
        print()
        execute_all_runs()
    else:
        print(f"\nExecuting single run: {args.run}")
        passed = execute_run(args.run)
        print()
        print(f"Run {args.run}: {'PASSED' if passed else 'FAILED'}")


if __name__ == "__main__":
    main()
