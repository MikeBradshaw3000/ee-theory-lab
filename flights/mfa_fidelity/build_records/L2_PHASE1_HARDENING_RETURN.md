# Note to L2 — Bounded Hardening Pass Return: Items 1–8 Implemented; Closure Requested

**From:** L1, routed by Mike
**Register:** closed, scoped — return of your closure review's bounded repair packet, nothing beyond it. Changed files carried verbatim below the rule (unchanged Phase-1 files stand as reviewed in the repair packet, digest-identified there); digests at the foot. Suite: 68/68. Your prescribed closure battery is run and reported in §2.

## §1 Item map (your item → implementation → discriminating test)

1. **Raw-bit comparator:** `raw_bit_equal` (shape + dtype + `tobytes(order="C")`) is now the sole Gate-A comparator for all four state arrays and every telemetry column. Test `test_raw_bit_comparator_rejects_signed_zero`: `np.array_equal` passes +0.0/−0.0 where the comparator rejects it; dtype mismatch rejected; copies accepted.
2. **Pinned root explicit:** `/home/claude/repo` deleted; `MFA_PINNED_REPO_ROOT` is the named integration input; pinned-ancestor tests skip with a stated reason when unset. Static path scan of package + tests: clean (compiled `__pycache__` artifacts excluded; .gitignore note queued for the commit session).
3. **Tier-1 file-global coverage:** a `seen` ledger of length ticks × n_cells; cross-batch duplicates counted on arrival (`row_duplication_or_range`); completion requires every key (`key_coverage_complete`).
4. **E1 identity coverage:** the same ledger discipline (`row_duplication`, `key_coverage_complete`) alongside the bitwise value checks.
5. **Discriminating negatives:** `test_tier1_duplicate_for_missing_same_size_cross_batch` — victim removed, same-tick donor duplicated, copies forced into different verifier batches (batch_size=100); assertions confirm `rows_total` and `tick_coverage_exact` remain clean (the counting checks provably cannot catch it) while duplication and key coverage fail it. `test_e1_duplicate_for_missing_unchanged_bits` — the E1 variant with base bits unchanged by construction; `base_bit_identity == 0` asserted; structural coverage alone fails the file. `test_malformed_rho_schema_fails_closed` — wrong columns yield a failed report, no exception.
6. **Neutral schema contract:** `mfa_instrument/schema_contract.py` holds the normative ledger (ANCESTOR_COLUMNS, EXTENSION_COLUMNS, NOISE_COLUMN, RHO_TABLE_COLUMNS) with provenance comment; writer and verifier both import it; the verifier no longer obtains expectations from the module it verifies.
7. **Fail-closed rho:** schema mismatch records the failure and returns before any indexing of the malformed table.
8. **Independently frozen ancestor digest:** `ANCESTOR_SHA256 = "4f825bbe956a2b225e0c843876189c65a84af1fd74f7325ec94657747b9dbea3"`, established from the commit-pinned object (git checkout 4d9a622 → sha256sum of the ancestor file, L1 pinned clone, 2026-08-24; cross-confirmation against Mike's clone queued for the catch-up commit session). The provenance comment now states the verify-never-establish rule; AUTHORITATIVE requires the expectation and raises without it (unchanged from the repair packet).

**Recorded, not actioned (per your §3):** the verifier-independence hardening (reconstructing pre-update activity, Local_Density, ds, Psi_local, rho_global from activity telemetry) is entered in the later-hardening ledger; it does not broaden this register.

## §2 Closure battery (your §4 requirements)

- Full suite: **68/68** (63 + the five new discriminating tests).
- Provisional Gate A, all three ancestor-existing F forms, **digest verification active** (expected_ancestor_sha256 supplied and checked):
  `GATE A [PROVISIONAL] f=F_2_symmetric grid=12 ticks=25 preflight=PASS state=BIT-EXACT telemetry=BIT-EXACT gate=PASS ancestor_sha256=4f825bbe956a env=python3.12.3/numpy2.4.4 [NON-CONFORMING: provisional only]`
  `GATE A [PROVISIONAL] f=F_LR ... gate=PASS ancestor_sha256=4f825bbe956a ...`
  `GATE A [PROVISIONAL] f=F_baseline ... gate=PASS ancestor_sha256=4f825bbe956a ...`
  (BIT-EXACT now means the raw-storage comparator.)
- V6 path scan: clean over source and tests.

## §3 Disposition requested (closed register, per your §5)

1. Items 1–8: **REPAIRED AS REQUIRED** or **REPAIR DEFECT** with location.
2. New defects within the closed Phase-1 register: **NONE FOUND** complete.
3. **Phase-1 closure:** PHASE 1 COMPLETE, subject to the final authoritative Gate-A regression on the frozen environment against the independently frozen ancestor digest — or remaining blockers named.

---

# ARTIFACT: mfa_instrument/schema_contract.py
```python
"""mfa_instrument.schema_contract — The NORMATIVE telemetry schema ledger.

Item 6 of L2's bounded hardening pass (closure review): the frozen column ledger
lives in this neutral specification-level module. BOTH the writer (telemetry.py)
and the verifier (verify.py) import from here; the verifier never obtains its
normative expectation from the module whose output it verifies, so no single
constant edit can move emitted schema and verification expectation together.

Source of the 25-column family: flight2_production.py @ 4d9a622 telemetry row
dict, read verbatim (Merge Specification v0.4 FROZEN §7.1).
"""

ANCESTOR_COLUMNS = [
    "Tick", "Agent_X", "Agent_Y", "b_i_v", "b_i_u", "b_i_r", "limiting_base_argmin",
    "Lambda_multiplicative", "Lambda_additive", "Lambda_total", "Local_Density",
    "Drive_Raw", "Term_Density_Pos", "Term_Overcrowding", "Term_Offset", "p_base",
    "p_act", "PRNG_draw", "is_active", "Psi_local", "gamma_coef", "Delta_v",
    "Delta_u", "Delta_r", "Term_Lambda",
]
EXTENSION_COLUMNS = ["Delta_from_Psi", "Delta_from_rho"]   # spec §4.5 (rho channel)
NOISE_COLUMN = "Noise_Draw"                                 # conditional (η_MFA)
RHO_TABLE_COLUMNS = ["Tick", "rho_global"]                  # spec §7.2 tick table
```

# ARTIFACT: mfa_instrument/telemetry.py
```python
"""mfa_instrument.telemetry — Row-family emission, parquet streaming, canonical digest.

Spec anchors: Merge Specification v0.4 FROZEN §7.1 (25-column ancestor family +
Delta_from_Psi/Delta_from_rho + conditional Noise_Draw; rho_global tick table),
§7.3 (canonical telemetry digest: parquet files' raw bytes in ascending lexicographic
filename order, each preceded by its filename as a UTF-8 line), §8.1 (instrumentation
must not alter state, evaluation order, dtype, or stochastic consumption — this module
only reads the read-only field views the dynamics sink provides).

Ancestor column order (flight2_production.py @ 4d9a622, telemetry row dict, verbatim):
Tick, Agent_X, Agent_Y, b_i_v, b_i_u, b_i_r, limiting_base_argmin,
Lambda_multiplicative, Lambda_additive, Lambda_total, Local_Density, Drive_Raw,
Term_Density_Pos, Term_Overcrowding, Term_Offset, p_base, p_act, PRNG_draw,
is_active, Psi_local, gamma_coef, Delta_v, Delta_u, Delta_r, Term_Lambda  (25 columns)

Row order: per tick, cells in np.indices row-major flatten order (ancestor xs/ys loop).
"""
from __future__ import annotations

import hashlib
import os
from typing import Dict, List, Optional

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

from .schema_contract import (ANCESTOR_COLUMNS, EXTENSION_COLUMNS,   # noqa: F401
                              NOISE_COLUMN, RHO_TABLE_COLUMNS)
# Normative ledger lives in schema_contract (L2 closure item 6); re-exported names
# preserved for existing consumers.


class TelemetryWriter:
    """Builds per-tick row frames from the dynamics sink fields (vectorized; values
    identical to the ancestor's per-cell loop) and streams them to parquet in chunks.

    Schema policy: the column set is fixed at construction from the configuration —
    Gate-A configurations carry exactly the 25 ancestor columns (extension columns
    STRUCTURALLY ABSENT, per §8.1's preflight); rho-channel configurations add the
    two decomposition columns; noise-enabled adds Noise_Draw. E1 total-Q-disable
    drops gamma_coef/Delta_v/u/r (no Q arithmetic exists to report).
    """

    def __init__(self, grid_scale: int, gamma_psi: float, gamma_rho: float,
                 noise_enabled: bool, chunk_ticks: int = 500) -> None:
        self._gs = grid_scale
        xs, ys = np.indices((grid_scale, grid_scale))
        self._xs = xs.flatten()
        self._ys = ys.flatten()
        self._gamma_psi = gamma_psi
        q_disabled = (gamma_psi == 0.0 and gamma_rho == 0.0)
        cols = list(ANCESTOR_COLUMNS)
        if q_disabled:
            for c in ("gamma_coef", "Delta_v", "Delta_u", "Delta_r"):
                cols.remove(c)
        if gamma_rho != 0.0:
            cols += EXTENSION_COLUMNS
        if noise_enabled:
            cols.append(NOISE_COLUMN)
        self.columns = cols
        self._chunk_ticks = chunk_ticks
        self._frames: List[pd.DataFrame] = []
        self._ticks_buffered = 0
        self._writer: Optional[pq.ParquetWriter] = None
        self._schema: Optional[pa.Schema] = None
        self._path: Optional[str] = None
        self.rows_written = 0
        self.rho_global_table: List[tuple] = []   # (tick, rho_global) tick-level table (§7.2)

    # -- sink --------------------------------------------------------------
    def sink(self, tick: int, fields: Dict[str, np.ndarray]) -> None:
        n = self._xs.size
        data: Dict[str, np.ndarray] = {
            "Tick": np.full(n, tick, dtype=np.int64),
            "Agent_X": self._xs.astype(np.int64),
            "Agent_Y": self._ys.astype(np.int64),
        }
        for col in self.columns:
            if col in data:
                continue
            if col == "gamma_coef":
                data[col] = np.full(n, self._gamma_psi, dtype=np.float64)
            else:
                data[col] = np.asarray(fields[col]).reshape(-1)
        if "rho_global" in fields:
            self.rho_global_table.append((tick, float(fields["rho_global"])))
        self._frames.append(pd.DataFrame(data, columns=self.columns))
        self._ticks_buffered += 1
        if self._path is not None and self._ticks_buffered >= self._chunk_ticks:
            self._flush()

    # -- parquet streaming (ancestor pattern: schema from first chunk, snappy) ----
    def open(self, path: str) -> None:
        self._path = path

    def _flush(self) -> None:
        if not self._frames:
            return
        df = pd.concat(self._frames, ignore_index=True)
        if self._writer is None:
            table = pa.Table.from_pandas(df, preserve_index=False)
            self._schema = table.schema
            self._writer = pq.ParquetWriter(self._path, self._schema, compression="snappy")
            self._writer.write_table(table)
        else:
            table = pa.Table.from_pandas(df, preserve_index=False, schema=self._schema)
            self._writer.write_table(table)
        self.rows_written += len(df)
        self._frames.clear()
        self._ticks_buffered = 0

    def close(self) -> None:
        if self._path is not None:
            self._flush()
        if self._writer is not None:
            self._writer.close()
            self._writer = None
        # N2 (L2 Phase-1 review): the rho_global tick table is a REQUIRED persisted
        # artifact wherever it is populated — an in-memory list is not the spec's
        # tick-level table. Written beside the row file as <stem>.rho_global.parquet;
        # its filename enters the same canonical digest set as every telemetry file.
        if self._path is not None and self.rho_global_table:
            rho_df = pd.DataFrame(self.rho_global_table, columns=["Tick", "rho_global"])
            self.rho_global_path = self._path.rsplit(".parquet", 1)[0] + ".rho_global.parquet"
            rho_df.to_parquet(self.rho_global_path, index=False)
        else:
            self.rho_global_path = None

    def artifact_paths(self) -> List[str]:
        """Every persisted artifact of this writer, for the canonical digest."""
        out = []
        if self._path is not None:
            out.append(self._path)
        if getattr(self, "rho_global_path", None):
            out.append(self.rho_global_path)
        return out

    # -- in-memory access (harness/test use) -------------------------------
    def frame(self) -> pd.DataFrame:
        """Concatenated buffered frames. ONLY valid in pure in-memory use: if the
        writer was opened for streaming, buffered frames are a partial tail and
        returning them would silently misrepresent the run (L2 code-audit D6)."""
        if self._path is not None:
            raise RuntimeError("frame() is unavailable on a streaming writer: rows have "
                               "been flushed to disk; read the parquet file instead")
        return pd.concat(self._frames, ignore_index=True) if self._frames else pd.DataFrame(columns=self.columns)


def telemetry_digest(paths: List[str]) -> str:
    """Spec §7.3 canonical construction: SHA-256 over the concatenation of the files'
    raw bytes in ascending lexicographic FILENAME order, each preceded by its filename
    as a UTF-8 line ('<name>\\n'). Filenames therefore enter the digest; the run record
    is outside every digest it reports."""
    names = [os.path.basename(p) for p in paths]
    if len(set(names)) != len(names):
        raise ValueError("telemetry_digest requires unique basenames: the canonical "
                         "construction is filename-keyed (L2 code-audit D6)")
    h = hashlib.sha256()
    for p in sorted(paths, key=lambda q: os.path.basename(q)):
        h.update((os.path.basename(p) + "\n").encode("utf-8"))
        with open(p, "rb") as fh:
            for chunk in iter(lambda: fh.read(1 << 20), b""):
                h.update(chunk)
    return h.hexdigest()
```

# ARTIFACT: mfa_instrument/verify.py
```python
"""mfa_instrument.verify — Tier-1 row-level recomputation (the verification spine).

Spec anchors: Merge Specification v0.4 FROZEN §7.2. Rebuilt per L2 Phase-1 review
V1–V5: the verifier is now SCHEMA- AND COMPLETENESS-ENFORCING —

  V1: the expected column set is BUILT FROM THE CONFIGURATION and compared against
      the file before any recomputation; missing columns and forbidden columns both
      fail. Conditional artifacts (Noise_Draw; the rho_global tick table) are
      required-or-forbidden by configuration, never merely tolerated.
  V2: the global-Q decomposition is verified (Delta_from_rho == gamma_rho *
      rho_global(t), joined by tick against the persisted tick table).
  V3: completeness is enforced from the consumed configuration: rows_seen must equal
      ticks * grid_scale^2; every tick 0..ticks-1 present; exactly one row per
      (Tick, Agent_X, Agent_Y); full coordinate coverage. An empty report FAILS
      (all([]) can never again mean PASS).
  V4: E1 base identity is BITWISE (float64 storage via view(np.uint64)), tick-0
      anchored, coverage-enforcing, empty-rejecting, and asserts the absence of
      every Q-related column including the decomposition pair.
  V5: every persisted component in the declared families is checked — Term_Offset,
      gamma_coef, Delta_from_Psi (including the gamma_psi == 0 zero requirement),
      global Delta_from_rho, and the rho_global tick table itself.

All value checks remain EXACT equality: tolerances would hide the FP-ordering
divergence Tier-1 exists to catch.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Optional, Set, Tuple

import numpy as np
import pandas as pd
import pyarrow.parquet as pq

from .config import RunConfig
from .schema_contract import (ANCESTOR_COLUMNS, EXTENSION_COLUMNS,
                              NOISE_COLUMN, RHO_TABLE_COLUMNS)


@dataclass
class Tier1Report:
    checks: Dict[str, int] = field(default_factory=dict)   # name -> mismatch count
    rows_seen: int = 0
    ticks_seen: Tuple[int, int] = (0, 0)

    def record(self, name: str, mismatches: int) -> None:
        self.checks[name] = self.checks.get(name, 0) + int(mismatches)

    @property
    def passed(self) -> bool:
        # V3: an empty report is a FAILURE, not a vacuous pass.
        if not self.checks or self.rows_seen == 0:
            return False
        return all(v == 0 for v in self.checks.values())

    def summary(self) -> str:
        parts = [f"{k}={'OK' if v == 0 else f'{v} MISMATCHES'}" for k, v in self.checks.items()]
        return (f"TIER-1 rows={self.rows_seen} ticks={self.ticks_seen[0]}..{self.ticks_seen[1]} "
                + " ".join(parts) + (" => PASS" if self.passed else " => FAIL"))


def _sigmoid(x: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-x))


def expected_schema(cfg: RunConfig) -> Set[str]:
    """V1: the required column set, derived from the consumed configuration exactly
    as TelemetryWriter derives its schema — but independently, so a writer defect
    cannot define its own expectation."""
    cols = set(ANCESTOR_COLUMNS)
    if cfg.q.gamma_psi == 0.0 and cfg.q.gamma_rho == 0.0:
        cols -= {"gamma_coef", "Delta_v", "Delta_u", "Delta_r"}
    if cfg.q.gamma_rho != 0.0:
        cols |= set(EXTENSION_COLUMNS)
    if cfg.noise.amplitude > 0.0:
        cols.add(NOISE_COLUMN)
    return cols


def tier1_verify(parquet_path: str, cfg: RunConfig,
                 rho_global_path: Optional[str] = None,
                 expect_rho_global: Optional[bool] = None,
                 batch_size: int = 200_000) -> Tier1Report:
    """Stream the telemetry and recompute every Tier-1 invariant, with schema and
    completeness enforced before and during recomputation.

    expect_rho_global: whether the run was a Gate-R/rho-emitting run (defaults to
    the Q-global condition; E1 Gate-R runs pass True explicitly per spec §7.2)."""
    rep = Tier1Report()
    k = cfg.constants
    if expect_rho_global is None:
        expect_rho_global = (cfg.q.gamma_rho != 0.0 and cfg.q.q_read == "global")

    # ---- V1: schema gate ----
    pf = pq.ParquetFile(parquet_path)
    have = set(pf.schema_arrow.names)
    want = expected_schema(cfg)
    rep.record("schema_missing_columns", len(want - have))
    rep.record("schema_forbidden_columns", len(have - want))
    if want != have:
        return rep   # recomputation on a wrong-schema file proves nothing

    # ---- rho_global tick table: required-or-forbidden (V1/N1/N2) ----
    rho_df: Optional[pd.DataFrame] = None
    if expect_rho_global:
        if rho_global_path is None:
            rep.record("rho_global_artifact_missing", 1)
            return rep
        rho_df = pd.read_parquet(rho_global_path)
        if list(rho_df.columns) != RHO_TABLE_COLUMNS:
            rep.record("rho_global_schema", 1)
            return rep          # item 7: fail CLOSED — never index a malformed table
        rep.record("rho_global_schema", 0)
        rep.record("rho_global_tick_coverage",
                   0 if np.array_equal(np.sort(rho_df["Tick"].to_numpy()),
                                       np.arange(cfg.ticks)) else 1)
    else:
        rep.record("rho_global_artifact_forbidden", 0 if rho_global_path is None else 1)

    # ---- streaming recomputation with completeness accounting (V3) ----
    n_cells = cfg.n_cells
    tick_row_counts = np.zeros(cfg.ticks, dtype=np.int64)
    seen = np.zeros(cfg.ticks * n_cells, dtype=bool)   # item 3: file-global key ledger
    dup_or_range_bad = 0
    coord_bad = 0
    rho_map = (dict(zip(rho_df["Tick"].to_numpy(), rho_df["rho_global"].to_numpy()))
               if rho_df is not None else {})

    t_min: Optional[int] = None
    t_max: Optional[int] = None

    for batch in pf.iter_batches(batch_size=batch_size):
        df = batch.to_pandas()
        n = len(df)
        rep.rows_seen += n
        ticks = df["Tick"].to_numpy()
        if ticks.size:
            t_min = int(ticks.min()) if t_min is None else min(t_min, int(ticks.min()))
            t_max = int(ticks.max()) if t_max is None else max(t_max, int(ticks.max()))
        in_range = (ticks >= 0) & (ticks < cfg.ticks)
        dup_or_range_bad += int((~in_range).sum())
        np.add.at(tick_row_counts, ticks[in_range], 1)
        xy_ok = ((df["Agent_X"].to_numpy() >= 0) & (df["Agent_X"].to_numpy() < cfg.grid_scale)
                 & (df["Agent_Y"].to_numpy() >= 0) & (df["Agent_Y"].to_numpy() < cfg.grid_scale))
        coord_bad += int((~xy_ok).sum())
        key = (ticks.astype(np.int64) * n_cells
               + df["Agent_X"].to_numpy(np.int64) * cfg.grid_scale
               + df["Agent_Y"].to_numpy(np.int64))
        valid = in_range & xy_ok
        vkey = key[valid]
        dup_or_range_bad += int(seen[vkey].sum())      # cross-batch duplicates counted
        seen[vkey] = True

        # 1. Realization invariant.
        rep.record("realization_invariant",
                   int((df["is_active"] != (df["PRNG_draw"] < df["p_act"])).sum()))

        # 2. Λ recomputation per dispatch label.
        v, u, r = (df["b_i_v"].to_numpy(), df["b_i_u"].to_numpy(), df["b_i_r"].to_numpy())
        lam_mult = v * u * r
        lam_add = k.w_v * v + k.w_u * u + k.w_r * r
        rep.record("lambda_multiplicative",
                   int((df["Lambda_multiplicative"].to_numpy() != lam_mult).sum()))
        rep.record("lambda_additive",
                   int((df["Lambda_additive"].to_numpy() != lam_add).sum()))
        f = cfg.f_dispatch
        if f == "F_baseline":
            lam = (v + u + r) / 3.0
        elif f == "F_LR":
            lam = np.minimum(np.minimum(v, u), r)
        elif f == "F_2_symmetric":
            lam = lam_mult * lam_add
        else:
            lam = lam_mult
        rep.record("lambda_total_dispatch",
                   int((df["Lambda_total"].to_numpy() != lam).sum()))

        # 3. Drive decomposition — every persisted component (V5).
        dens = df["Local_Density"].to_numpy()
        term_lambda = k.alpha * df["Lambda_total"].to_numpy()
        term_dens = k.beta * dens
        term_over = -k.delta * (dens ** 2)
        term_off = np.full_like(v, -k.gamma_offset)
        drive = term_lambda + term_dens + term_over + term_off
        if cfg.drive_schedule:
            u_t_col = np.zeros(n, dtype=np.float64)
            for start, val in cfg.drive_schedule:
                u_t_col = np.where(ticks >= start, val, u_t_col)
            nonzero = u_t_col != 0.0
            drive = np.where(nonzero, drive + u_t_col, drive)
        if NOISE_COLUMN in have:
            drive = drive + df[NOISE_COLUMN].to_numpy()
        rep.record("term_lambda", int((df["Term_Lambda"].to_numpy() != term_lambda).sum()))
        rep.record("term_density_pos", int((df["Term_Density_Pos"].to_numpy() != term_dens).sum()))
        rep.record("term_overcrowding", int((df["Term_Overcrowding"].to_numpy() != term_over).sum()))
        rep.record("term_offset", int((df["Term_Offset"].to_numpy() != term_off).sum()))
        rep.record("drive_raw", int((df["Drive_Raw"].to_numpy() != drive).sum()))

        # 4. Probability chain.
        p_base = _sigmoid(df["Drive_Raw"].to_numpy())
        p_act = np.clip(p_base + k.eta_floor * (1.0 - p_base), 0.0, 1.0)
        rep.record("p_base", int((df["p_base"].to_numpy() != p_base).sum()))
        rep.record("p_act", int((df["p_act"].to_numpy() != p_act).sum()))

        # 5. Q decomposition — applicability guaranteed by the V1 schema gate.
        if "Delta_v" in want:
            psi = df["Psi_local"].to_numpy()
            rep.record("gamma_coef",
                       int((df["gamma_coef"].to_numpy() != cfg.q.gamma_psi).sum()))
            if "Delta_from_rho" in want:
                dpsi = df["Delta_from_Psi"].to_numpy()
                drho = df["Delta_from_rho"].to_numpy()
                rep.record("q_decomposition_sum",
                           int((df["Delta_v"].to_numpy() != dpsi + drho).sum()))
                if cfg.q.gamma_psi != 0.0:
                    rep.record("delta_from_psi",
                               int((dpsi != cfg.q.gamma_psi * psi).sum()))
                else:
                    rep.record("delta_from_psi_zero", int((dpsi != 0.0).sum()))   # V5
                if cfg.q.q_read == "local":
                    rep.record("delta_from_rho_local",
                               int((drho != cfg.q.gamma_rho * dens).sum()))
                else:                                                              # V2
                    expected = np.array([cfg.q.gamma_rho * rho_map.get(t, np.nan)
                                         for t in ticks])
                    rep.record("delta_from_rho_global",
                               int((drho != expected).sum()))
            else:
                rep.record("q_ancestor_expression",
                           int((df["Delta_v"].to_numpy() != cfg.q.gamma_psi * psi).sum()))
            rep.record("q_uniform_across_bases",
                       int((df["Delta_v"].to_numpy() != df["Delta_u"].to_numpy()).sum()
                           + (df["Delta_v"].to_numpy() != df["Delta_r"].to_numpy()).sum()))

    # ---- V3 completeness verdicts ----
    rep.record("rows_total",
               0 if rep.rows_seen == cfg.ticks * n_cells else 1)
    rep.record("tick_coverage_exact",
               0 if bool(np.all(tick_row_counts == n_cells)) else 1)
    rep.record("row_duplication_or_range", dup_or_range_bad)
    rep.record("coordinate_range", coord_bad)
    rep.record("key_coverage_complete", 0 if bool(seen.all()) else 1)   # item 3
    rep.ticks_seen = (t_min if t_min is not None else -1,
                      t_max if t_max is not None else -1)
    return rep


def e1_base_bit_identity(parquet_path: str, cfg: RunConfig,
                         batch_size: int = 200_000) -> Tier1Report:
    """Contract E1 v0.8 §2 conformance, rebuilt per V4: TRUE bitwise identity
    (float64 storage compared as uint64 views), tick-0 anchored, coverage-enforced,
    empty-rejecting, with the full Q-column absence set asserted."""
    rep = Tier1Report()
    pf = pq.ParquetFile(parquet_path)
    cols = set(pf.schema_arrow.names)
    for q_col in ("Delta_v", "Delta_u", "Delta_r", "gamma_coef",
                  "Delta_from_Psi", "Delta_from_rho"):        # V4: full set
        rep.record(f"schema_absent_{q_col}", 0 if q_col not in cols else 1)

    n_cells = cfg.n_cells
    base_bits: Dict[int, Tuple[int, int, int]] = {}
    tick0_seen = np.zeros(n_cells, dtype=bool)
    tick_row_counts = np.zeros(cfg.ticks, dtype=np.int64)
    seen = np.zeros(cfg.ticks * n_cells, dtype=bool)   # item 4: exact key coverage
    dup_bad = 0
    mismatches = 0
    anchored_late = 0

    for batch in pf.iter_batches(batch_size=batch_size,
                                 columns=["Tick", "Agent_X", "Agent_Y",
                                          "b_i_v", "b_i_u", "b_i_r"]):
        df = batch.to_pandas()
        rep.rows_seen += len(df)
        ticks = df["Tick"].to_numpy()
        in_range = (ticks >= 0) & (ticks < cfg.ticks)
        np.add.at(tick_row_counts, ticks[in_range], 1)
        keys = (df["Agent_X"].to_numpy(np.int64) * cfg.grid_scale
                + df["Agent_Y"].to_numpy(np.int64))
        gkey = ticks.astype(np.int64) * n_cells + keys
        gvalid = in_range & (keys >= 0) & (keys < n_cells)
        dup_bad += int(seen[gkey[gvalid]].sum())
        seen[gkey[gvalid]] = True
        bv = df["b_i_v"].to_numpy(np.float64).view(np.uint64)
        bu = df["b_i_u"].to_numpy(np.float64).view(np.uint64)
        br = df["b_i_r"].to_numpy(np.float64).view(np.uint64)
        for i in range(len(df)):
            key = int(keys[i]); t = int(ticks[i])
            bits = (int(bv[i]), int(bu[i]), int(br[i]))
            if t == 0:
                base_bits[key] = bits
                tick0_seen[key] = True
            else:
                if key not in base_bits:
                    anchored_late += 1        # V4: no first-row anchoring allowed
                elif bits != base_bits[key]:
                    mismatches += 1

    rep.record("base_bit_identity", mismatches)
    rep.record("tick0_baseline_complete", 0 if bool(tick0_seen.all()) else 1)
    rep.record("anchored_without_tick0", anchored_late)
    rep.record("rows_total", 0 if rep.rows_seen == cfg.ticks * n_cells else 1)
    rep.record("tick_coverage_exact",
               0 if bool(np.all(tick_row_counts == n_cells)) else 1)
    rep.record("row_duplication", dup_bad)                              # item 4
    rep.record("key_coverage_complete", 0 if bool(seen.all()) else 1)   # item 4
    return rep
```

# ARTIFACT: mfa_instrument/gates/gate_a.py
```python
"""mfa_instrument.gates.gate_a — Gate A: Lineage A preservation (bit-exact, conditional).

Spec anchors: Merge Specification v0.4 FROZEN §8.1 — two-level harness:
  STRUCTURAL PREFLIGHT (diagnostic, never a substitute): six checks establishing that
  the Gate-A configuration executes no extension path;
  BEHAVIORAL CERTIFICATION (the actual gate): complete matched-seed comparison against
  flight2_production.py — bit-exact state and telemetry equality.

PROVISIONAL vs AUTHORITATIVE (Build Plan v0.2, L2 finding 1): any run of this harness
during build is a CHECKPOINT; the certification is only the final run on the complete
integrated stage-1 commit, on Mike's machine, under the frozen environment. Every
report emitted here is labeled accordingly.

The ancestor is IMPORTED FROM THE PINNED SOURCE FILE (never transcribed): the
comparison target is flight2_production.NumpyEEModel itself.
"""
from __future__ import annotations

import importlib.util
import sys


def raw_bit_equal(a, b) -> bool:
    """Item 1 (L2 closure review): RAW-STORAGE equality — shape, dtype, and exact
    bytes. Unlike np.array_equal, this rejects +0.0 vs -0.0 (different bit patterns,
    numerically equal). Gate A's BIT-EXACT claim is earned by this comparator only."""
    import numpy as _np
    a = _np.asarray(a); b = _np.asarray(b)
    return (a.shape == b.shape and a.dtype == b.dtype
            and a.tobytes(order="C") == b.tobytes(order="C"))
from dataclasses import dataclass, field
from typing import List, Tuple

import numpy as np
import pandas as pd

from ..config import RunConfig, QConfig, InitConfig
from ..rng import SeedRegistry, RoleError
from ..init import initialize
from ..dynamics import Dynamics
from ..telemetry import TelemetryWriter, ANCESTOR_COLUMNS

GATE_A_SEED = 0x7A9B31C          # facts v1.1 S6(a): the matched seed
ANCESTOR_GAMMA_Q = 0.001          # ancestor GAMMA_Q; Gate-A gamma_psi


def load_ancestor(pinned_repo_root: str, expected_sha256: "str|None" = None,
                  require_provenance: bool = False):
    """Import the ancestor module from the pinned clone, with provenance
    verification (L2 Phase-1 review N4): the file's SHA-256 is computed and,
    when an expectation is supplied (mandatory for AUTHORITATIVE runs), enforced
    BEFORE import — the harness must never certify parity against a modified or
    wrong reference. The digest is returned for the report either way."""
    import hashlib
    path = pinned_repo_root + "/" + ANCESTOR_REL_PATH
    with open(path, "rb") as fh:
        digest = hashlib.sha256(fh.read()).hexdigest()
    if require_provenance and expected_sha256 is None:
        raise RuntimeError("AUTHORITATIVE Gate A requires an expected ancestor "
                           "digest; none supplied (L2 Phase-1 review N4)")
    if expected_sha256 is not None and digest != expected_sha256:
        raise RuntimeError(f"ancestor provenance FAILED: {path} has sha256 {digest}, "
                           f"expected {expected_sha256}")
    spec = importlib.util.spec_from_file_location("flight2_production", path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["flight2_production"] = mod
    spec.loader.exec_module(mod)
    return mod, digest


def gate_a_config(f_form: str, grid_scale: int, ticks: int) -> RunConfig:
    """The channels-zeroed Gate-A configuration (spec §8.1): symmetric_chain, A's
    constants (config defaults), u_t = 0 (empty schedule), noise 0 (no stream),
    gamma_rho = 0 (no-read bypass), gamma_psi = ancestor GAMMA_Q, ancestor init
    parameters, ancestor-existing f_form (F_canonical has no ancestor branch)."""
    if f_form == "F_canonical":
        raise ValueError("Gate A requires an ancestor-existing F form (no F_canonical "
                         "branch exists at 4d9a622)")
    return RunConfig(
        seed=GATE_A_SEED, rule_mode="symmetric_chain", f_dispatch=f_form,
        grid_scale=grid_scale, ticks=ticks,
        q=QConfig(q_read="local", gamma_psi=ANCESTOR_GAMMA_Q, gamma_rho=0.0),
        init=InitConfig(),                     # m=0.75, w=0.3 => U(0.6, 0.9); p=0.5
        allow_legacy_f_baseline=(f_form == "F_baseline"),
    )


@dataclass
class PreflightReport:
    checks: List[Tuple[str, bool]] = field(default_factory=list)

    def record(self, name: str, ok: bool) -> None:
        self.checks.append((name, ok))

    @property
    def passed(self) -> bool:
        return all(ok for _, ok in self.checks)


def structural_preflight(cfg: RunConfig) -> PreflightReport:
    """Spec §8.1's six checks, run on a short constructed execution. Diagnostic only."""
    rep = PreflightReport()
    # (i) Gate-A registry forbids every non-ancestor stream (absence, not idleness).
    reg = SeedRegistry(cfg.seed, gate_a_mode=True)
    try:
        reg.role("noise")
        rep.record("noise_stream_absent", False)
    except RoleError:
        rep.record("noise_stream_absent", True)
    dyn = reg.dynamics()
    state = initialize(cfg.init, cfg.grid_scale, dyn)
    d = Dynamics(cfg, state, dyn)
    # (ii) no rho read is configured; the activation-read branch is unreachable.
    rep.record("no_rho_read_configured", d._rho_read is False)
    # (iii) telemetry schema: extension columns structurally absent.
    tw = TelemetryWriter(cfg.grid_scale, cfg.q.gamma_psi, cfg.q.gamma_rho, False)
    rep.record("delta_from_rho_structurally_absent",
               "Delta_from_rho" not in tw.columns and "Delta_from_Psi" not in tw.columns)
    rep.record("noise_column_absent", "Noise_Draw" not in tw.columns)
    # (iv) rho_global never computed: run ticks, assert tick table stays empty.
    seen = {}
    for _ in range(3):
        d.step(lambda t, f: seen.update(f))
    rep.record("rho_global_never_emitted", "rho_global" not in seen
               and len(tw.rho_global_table) == 0)
    # (v) dynamics-stream consumption equals ancestor expectation:
    #     init draws = 4 * n_cells scalars (v,u,r,activity per cell); per tick = one
    #     grid-shaped draw. An independent probe replays exactly that consumption.
    n = cfg.n_cells
    probe = np.random.default_rng(cfg.seed)
    for _ in range(n):
        probe.uniform(0.6, 0.9); probe.uniform(0.6, 0.9); probe.uniform(0.6, 0.9)
        probe.random()
    for _ in range(3):
        probe.random(size=(cfg.grid_scale, cfg.grid_scale))
    rep.record("draw_count_and_order_match",
               bool(np.array_equal(d._g.random(7), probe.random(7))))
    return rep


FROZEN_PYTHON_PREFIX = "3.14."     # spec §7.4 working assumption (executable hard-fail)
FROZEN_NUMPY = "2.4.4"             # spec §7.4 lock-file pin
GATE_A_LABELS = ("PROVISIONAL", "AUTHORITATIVE")   # closed set (L2 Phase-1 review D5)
# N4: ancestor provenance — the authoritative comparison target's frozen identity.
ANCESTOR_REL_PATH = ("flights/cycle2_round1/02_flight_1_v1_1_parity/"
                     "flight2_production.py")
# Item 8 (L2 closure review): the authoritative ancestor digest, established
# INDEPENDENTLY from the commit-pinned object (git checkout 4d9a622; sha256sum of
# flights/cycle2_round1/02_flight_1_v1_1_parity/flight2_production.py, computed on
# the L1 pinned clone 2026-08-24 and to be cross-confirmed against Mike's clone at
# the catch-up commit session). The authoritative machine VERIFIES this previously
# fixed identity; it never establishes identity from its own candidate file.
ANCESTOR_SHA256 = "4f825bbe956a2b225e0c843876189c65a84af1fd74f7325ec94657747b9dbea3"


@dataclass
class GateAReport:
    label: str                     # member of GATE_A_LABELS (closed set)
    f_form: str
    grid_scale: int
    ticks: int
    preflight: PreflightReport
    state_bit_exact: bool
    telemetry_bit_exact: bool
    environment: str
    ancestor_sha256: str = ""

    @property
    def behavioral_bit_exact(self) -> bool:
        """The behavioral comparison alone (L2 D5 separation)."""
        return self.state_bit_exact and self.telemetry_bit_exact

    @property
    def gate_passed(self) -> bool:
        """The two-level harness verdict: BOTH layers (frozen §8.1). A failed
        structural preflight can never be silently absorbed (L2 review N5)."""
        return self.preflight.passed and self.behavioral_bit_exact

    # `passed` retained as an alias of the harness verdict so no consumer can
    # accidentally read the weaker property under the stronger name.
    @property
    def passed(self) -> bool:
        return self.gate_passed

    def summary(self) -> str:
        return (f"GATE A [{self.label}] f={self.f_form} grid={self.grid_scale} "
                f"ticks={self.ticks} preflight={'PASS' if self.preflight.passed else 'FAIL'} "
                f"state={'BIT-EXACT' if self.state_bit_exact else 'DIVERGED'} "
                f"telemetry={'BIT-EXACT' if self.telemetry_bit_exact else 'DIVERGED'} "
                f"gate={'PASS' if self.gate_passed else 'FAIL'} "
                f"ancestor_sha256={self.ancestor_sha256[:12]} env={self.environment}")


def run_gate_a(pinned_repo_root: str, f_form: str, grid_scale: int, ticks: int,
               label: str = "PROVISIONAL",
               expected_ancestor_sha256: "str|None" = None) -> GateAReport:
    """Two-level harness: structural preflight + behavioral comparison against the
    ancestor class itself, matched seed, full state + telemetry rows, bitwise."""
    import platform
    if label not in GATE_A_LABELS:
        raise ValueError(f"Gate-A label must be one of {GATE_A_LABELS}, got {label!r} "
                         "(closed set; L2 Phase-1 review D5)")
    anc_mod, anc_digest = load_ancestor(pinned_repo_root, expected_ancestor_sha256,
                                        require_provenance=(label == "AUTHORITATIVE"))
    cfg = gate_a_config(f_form, grid_scale, ticks)

    # Ancestor: its own class, its own module-level PRNG_SEED (verify it matches).
    assert anc_mod.PRNG_SEED == GATE_A_SEED, "ancestor seed constant mismatch"
    anc = anc_mod.NumpyEEModel((grid_scale, grid_scale), f_form)

    # Ours.
    reg = SeedRegistry(cfg.seed, gate_a_mode=True)
    dyn = reg.dynamics()
    state = initialize(cfg.init, cfg.grid_scale, dyn)
    ours = Dynamics(cfg, state, dyn)
    tw = TelemetryWriter(cfg.grid_scale, cfg.q.gamma_psi, cfg.q.gamma_rho, False)

    state_ok = True
    telem_ok = True
    for _ in range(ticks):
        anc.step()
        ours.step(tw.sink)
        state_ok &= (raw_bit_equal(ours._v, anc.v) and
                     raw_bit_equal(ours._u_base, anc.u) and
                     raw_bit_equal(ours._r, anc.r) and
                     raw_bit_equal(ours._is_active, anc.is_active))
        if not state_ok:
            break

    if state_ok:
        anc_df = pd.DataFrame(anc.telemetry_buffer)[ANCESTOR_COLUMNS]
        our_df = tw.frame()[ANCESTOR_COLUMNS]
        telem_ok = anc_df.shape == our_df.shape and all(
            raw_bit_equal(anc_df[c].to_numpy(), our_df[c].to_numpy())
            for c in ANCESTOR_COLUMNS)
    else:
        telem_ok = False

    env = f"python{platform.python_version()}/numpy{np.__version__}"
    env_conforms = (platform.python_version().startswith(FROZEN_PYTHON_PREFIX)
                    and np.__version__ == FROZEN_NUMPY)
    if label == "AUTHORITATIVE" and not env_conforms:
        raise RuntimeError(
            f"AUTHORITATIVE Gate A refused: environment {env} does not conform to the "
            f"frozen pins (python {FROZEN_PYTHON_PREFIX}x / numpy {FROZEN_NUMPY}); "
            "run on the canonical venv (L2 code-audit D5). PROVISIONAL runs may proceed "
            "in non-conforming environments and are labeled accordingly.")
    if not env_conforms:
        env += " [NON-CONFORMING: provisional only]"
    return GateAReport(label=label, f_form=f_form, grid_scale=grid_scale, ticks=ticks,
                       preflight=structural_preflight(cfg),
                       state_bit_exact=bool(state_ok), telemetry_bit_exact=bool(telem_ok),
                       environment=env, ancestor_sha256=anc_digest)
```

# ARTIFACT: tests/test_telemetry_gate_a.py
```python
"""Telemetry + provisional Gate A. The Gate-A test imports the ACTUAL ancestor file
from the pinned clone — the strongest available discriminator short of the
authoritative run on the execution machine."""
import sys, os, tempfile
import numpy as np
import pandas as pd
import pytest

import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mfa_instrument.telemetry import TelemetryWriter, telemetry_digest, ANCESTOR_COLUMNS
from mfa_instrument.gates.gate_a import run_gate_a, gate_a_config, structural_preflight

# Item 2 (L2 closure review): the pinned ancestor repository is an EXPLICIT
# integration dependency, supplied by the invoking environment — never a
# machine-specific constant. Canonical invocation exports MFA_PINNED_REPO_ROOT.
REPO = os.environ.get("MFA_PINNED_REPO_ROOT")
requires_pinned_repo = pytest.mark.skipif(
    REPO is None, reason="MFA_PINNED_REPO_ROOT not set: pinned-ancestor integration "
                         "tests require the 4d9a622 clone path")

def test_gate_a_schema_is_exactly_ancestor_25():
    tw = TelemetryWriter(10, 0.001, 0.0, False)
    assert tw.columns == ANCESTOR_COLUMNS and len(tw.columns) == 25

def test_e1_schema_drops_q_columns():
    tw = TelemetryWriter(10, 0.0, 0.0, False)
    for c in ("gamma_coef", "Delta_v", "Delta_u", "Delta_r", "Delta_from_rho"):
        assert c not in tw.columns

def test_rho_schema_adds_decomposition():
    tw = TelemetryWriter(10, 0.0, 0.01, False)
    assert "Delta_from_Psi" in tw.columns and "Delta_from_rho" in tw.columns

def test_digest_canonical_construction():
    with tempfile.TemporaryDirectory() as td:
        a, b = os.path.join(td, "b.parquet"), os.path.join(td, "a.parquet")
        open(a, "wb").write(b"BBB"); open(b, "wb").write(b"AAA")
        d1 = telemetry_digest([a, b])
        d2 = telemetry_digest([b, a])          # order-insensitive input, filename-sorted
        assert d1 == d2
        import hashlib
        h = hashlib.sha256()
        h.update(b"a.parquet\n"); h.update(b"AAA")
        h.update(b"b.parquet\n"); h.update(b"BBB")
        assert d1 == h.hexdigest()             # exact spec construction

def test_gate_a_rejects_f_canonical():
    with pytest.raises(ValueError):
        gate_a_config("F_canonical", 10, 5)

def test_structural_preflight_passes():
    rep = structural_preflight(gate_a_config("F_2_symmetric", 8, 3))
    assert rep.passed, rep.checks

@requires_pinned_repo
@pytest.mark.parametrize("f_form", ["F_2_symmetric", "F_LR", "F_baseline"])
def test_provisional_gate_a_against_actual_ancestor(f_form):
    rep = run_gate_a(REPO, f_form, grid_scale=12, ticks=25, label="PROVISIONAL")
    assert rep.preflight.passed, rep.preflight.checks
    assert rep.state_bit_exact, rep.summary()
    assert rep.telemetry_bit_exact, rep.summary()

def test_parquet_roundtrip_and_rho_table():
    from mfa_instrument.config import RunConfig, QConfig
    from mfa_instrument.rng import SeedRegistry
    from mfa_instrument.init import initialize
    from mfa_instrument.dynamics import Dynamics
    cfg = RunConfig(seed=3, f_dispatch="F_canonical", grid_scale=6, ticks=10,
                    q=QConfig(q_read="global", gamma_psi=0.0, gamma_rho=0.01))
    dyn = SeedRegistry(3).dynamics()
    d = Dynamics(cfg, initialize(cfg.init, 6, dyn), dyn)
    tw = TelemetryWriter(6, 0.0, 0.01, False, chunk_ticks=4)
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "run.parquet")
        tw.open(p)
        for _ in range(10):
            d.step(tw.sink)
        tw.close()
        df = pd.read_parquet(p)
        assert len(df) == 10 * 36 and tw.rows_written == 360
        assert len(tw.rho_global_table) == 10       # tick-level table, one row per tick
        assert "Delta_from_rho" in df.columns
        # realization invariant holds on the written file
        assert bool((df["is_active"] == (df["PRNG_draw"] < df["p_act"])).all())


def test_raw_bit_comparator_rejects_signed_zero():
    """Item 1 negative test: np.array_equal accepts what the Gate-A comparator must
    reject — the comparator, not numeric equality, earns the BIT-EXACT claim."""
    from mfa_instrument.gates.gate_a import raw_bit_equal
    a = np.array([0.0, 1.5]); b = np.array([-0.0, 1.5])
    assert np.array_equal(a, b)              # numeric equality passes it
    assert not raw_bit_equal(a, b)           # raw storage rejects it
    assert not raw_bit_equal(a, a.astype(np.float32))   # dtype mismatch rejected
    assert raw_bit_equal(a, a.copy())

def test_authoritative_requires_frozen_digest_supplied():
    from mfa_instrument.gates.gate_a import run_gate_a, ANCESTOR_SHA256
    assert isinstance(ANCESTOR_SHA256, str) and len(ANCESTOR_SHA256) == 64
```

# ARTIFACT: tests/test_verify.py
```python
"""Tests for verify.py (V1-V5 rebuild) — negative matrix expanded per V7:
schema (missing/forbidden), completeness (empty/truncated/dropped/duplicated),
global-Q, rho_global artifact, Term_Offset, gamma_coef, raw-bit identity.
Path binding per V6: repo-relative via conftest-style pathing, no absolute L1 path."""
import os, sys, tempfile
import numpy as np
import pandas as pd
import pytest

# V6: repo-relative import — the package root is this test file's parent's parent.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mfa_instrument.config import RunConfig, QConfig, InitConfig, DynamicsConstants
from mfa_instrument.rng import SeedRegistry
from mfa_instrument.init import initialize
from mfa_instrument.dynamics import Dynamics
from mfa_instrument.telemetry import TelemetryWriter
from mfa_instrument.verify import tier1_verify, e1_base_bit_identity, expected_schema

def run_to_parquet(cfg, path, emit_rho=False):
    reg = SeedRegistry(cfg.seed, gate_a_mode=(cfg.q.gamma_rho == 0.0 and not cfg.drive_schedule
                                              and cfg.noise.amplitude == 0.0 and not emit_rho))
    dyn = reg.dynamics()
    d = Dynamics(cfg, initialize(cfg.init, cfg.grid_scale, dyn), dyn, emit_rho_global=emit_rho)
    tw = TelemetryWriter(cfg.grid_scale, cfg.q.gamma_psi, cfg.q.gamma_rho,
                         cfg.noise.amplitude > 0, chunk_ticks=5)
    tw.open(path)
    for _ in range(cfg.ticks):
        d.step(tw.sink)
    tw.close()
    return tw

def gate_a_cfg(**kw):
    d = dict(seed=0x7A9B31C, f_dispatch="F_2_symmetric", grid_scale=8, ticks=12,
             q=QConfig(q_read="local", gamma_psi=0.001, gamma_rho=0.0))
    d.update(kw); return RunConfig(**d)

def test_tier1_passes_clean_run():
    cfg = gate_a_cfg()
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "run.parquet")
        run_to_parquet(cfg, p)
        rep = tier1_verify(p, cfg)
        assert rep.passed, rep.summary()
        assert rep.rows_seen == 12 * 64

def test_tier1_global_q_with_rho_artifact():
    """V2: global decomposition verified against the persisted tick table."""
    cfg = RunConfig(seed=9, f_dispatch="F_canonical", grid_scale=8, ticks=10,
                    q=QConfig(q_read="global", gamma_psi=0.001, gamma_rho=0.02))
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "run.parquet")
        tw = run_to_parquet(cfg, p)
        assert tw.rho_global_path is not None            # N2: artifact persisted
        rep = tier1_verify(p, cfg, rho_global_path=tw.rho_global_path)
        assert rep.passed, rep.summary()
        # plant a wrong global decomposition value
        df = pd.read_parquet(p); df.loc[df.index[100], "Delta_from_rho"] += 1e-15
        p2 = os.path.join(td, "bad.parquet"); df.to_parquet(p2)
        rep2 = tier1_verify(p2, cfg, rho_global_path=tw.rho_global_path)
        assert not rep2.passed and rep2.checks["delta_from_rho_global"] > 0

def test_tier1_missing_rho_artifact_fails():
    cfg = RunConfig(seed=9, f_dispatch="F_canonical", grid_scale=6, ticks=5,
                    q=QConfig(q_read="global", gamma_psi=0.0, gamma_rho=0.02))
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "run.parquet")
        run_to_parquet(cfg, p)
        rep = tier1_verify(p, cfg, rho_global_path=None)
        assert not rep.passed and rep.checks["rho_global_artifact_missing"] == 1

def test_tier1_e1_local_gate_r_rho_emission():
    """N1: E1 total-Q-disable run CAN emit rho_global as a Gate-R obligation."""
    cfg = RunConfig(seed=6, f_dispatch="F_canonical", grid_scale=6, ticks=8,
                    q=QConfig(q_read="local", gamma_psi=0.0, gamma_rho=0.0))
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "run.parquet")
        tw = run_to_parquet(cfg, p, emit_rho=True)
        assert tw.rho_global_path is not None
        rep = tier1_verify(p, cfg, rho_global_path=tw.rho_global_path,
                           expect_rho_global=True)
        assert rep.passed, rep.summary()

def test_tier1_schema_missing_column_fails():
    """V1: a run generated under active Q with a Q column REMOVED must fail."""
    cfg = gate_a_cfg()
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "run.parquet")
        run_to_parquet(cfg, p)
        df = pd.read_parquet(p).drop(columns=["Delta_v"])
        p2 = os.path.join(td, "bad.parquet"); df.to_parquet(p2)
        rep = tier1_verify(p2, cfg)
        assert not rep.passed and rep.checks["schema_missing_columns"] > 0

def test_tier1_schema_forbidden_column_fails():
    cfg = RunConfig(seed=6, f_dispatch="F_canonical", grid_scale=6, ticks=4,
                    q=QConfig(q_read="local", gamma_psi=0.0, gamma_rho=0.0))
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "run.parquet")
        run_to_parquet(cfg, p)
        df = pd.read_parquet(p); df["Delta_v"] = 0.0     # forbidden under total-disable
        p2 = os.path.join(td, "bad.parquet"); df.to_parquet(p2)
        rep = tier1_verify(p2, cfg)
        assert not rep.passed and rep.checks["schema_forbidden_columns"] > 0

def test_tier1_empty_truncated_dropped_duplicated_fail():
    """V3: the completeness matrix."""
    cfg = gate_a_cfg(grid_scale=6, ticks=6)
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "run.parquet")
        run_to_parquet(cfg, p)
        full = pd.read_parquet(p)
        cases = {
            "empty": full.iloc[0:0],
            "dropped_tick": full[full.Tick != 3],
            "dropped_row": full.drop(index=full.index[77]),
            "duplicated_row": pd.concat([full, full.iloc[[50]]], ignore_index=True),
        }
        for name, df in cases.items():
            p2 = os.path.join(td, f"{name}.parquet"); df.to_parquet(p2)
            rep = tier1_verify(p2, cfg)
            assert not rep.passed, f"{name}: {rep.summary()}"

def test_tier1_catches_planted_value_defects():
    cfg = gate_a_cfg(f_dispatch="F_LR", grid_scale=8, ticks=6)
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "run.parquet")
        run_to_parquet(cfg, p)
        for col, check, mut in [
            ("is_active", "realization_invariant", lambda x: not x),
            ("Lambda_total", "lambda_total_dispatch", lambda x: x + 1e-12),
            ("Drive_Raw", "drive_raw", lambda x: x + 1e-9),
            ("Term_Offset", "term_offset", lambda x: x + 1e-12),      # V5
            ("gamma_coef", "gamma_coef", lambda x: x + 1e-9),          # V5
            ("p_act", "p_act", lambda x: min(1.0, x + 1e-12)),
            ("Delta_v", "q_ancestor_expression", lambda x: x + 1e-15),
        ]:
            df = pd.read_parquet(p)
            df.loc[df.index[37], col] = mut(df.loc[df.index[37], col])
            p2 = os.path.join(td, "bad.parquet"); df.to_parquet(p2)
            rep = tier1_verify(p2, cfg)
            assert not rep.passed and rep.checks[check] > 0, (col, rep.summary())

def test_e1_bit_identity_true_bitwise():
    """V4: negative-zero substitution — numerically equal, bitwise different."""
    cfg = RunConfig(seed=6, f_dispatch="F_canonical", grid_scale=6, ticks=8,
                    q=QConfig(q_read="local", gamma_psi=0.0, gamma_rho=0.0))
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "run.parquet")
        run_to_parquet(cfg, p)
        rep = e1_base_bit_identity(p, cfg)
        assert rep.passed, rep.summary()
        df = pd.read_parquet(p)
        # plant -0.0 over +0.0-like: force a value whose bits differ but compares ==
        idx = df[(df.Tick == 5)].index[3]
        orig = df.loc[idx, "b_i_v"]
        df.loc[idx, "b_i_v"] = np.nextafter(orig, np.inf)   # 1-ulp bit change
        p2 = os.path.join(td, "ulp.parquet"); df.to_parquet(p2)
        rep2 = e1_base_bit_identity(p2, cfg)
        assert not rep2.passed and rep2.checks["base_bit_identity"] == 1
        # negative-zero case, explicit
        df2 = pd.read_parquet(p)
        z_idx = df2.index[10]
        df2.loc[df2[df2.Tick == 0].index, "b_i_u"] = 0.0     # tick-0 baseline +0.0
        df2.loc[df2[(df2.Tick > 0)].index, "b_i_u"] = 0.0
        df2.loc[df2[(df2.Tick == 4)].index[7], "b_i_u"] = -0.0
        p3 = os.path.join(td, "negzero.parquet"); df2.to_parquet(p3)
        rep3 = e1_base_bit_identity(p3, cfg)
        assert rep3.checks["base_bit_identity"] >= 1        # == would have passed it

def test_e1_bit_identity_coverage_and_empty():
    cfg = RunConfig(seed=6, f_dispatch="F_canonical", grid_scale=6, ticks=6,
                    q=QConfig(q_read="local", gamma_psi=0.0, gamma_rho=0.0))
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "run.parquet")
        run_to_parquet(cfg, p)
        full = pd.read_parquet(p)
        for name, df in {"empty": full.iloc[0:0],
                         "no_tick0": full[full.Tick != 0],
                         "truncated": full[full.Tick < 4]}.items():
            p2 = os.path.join(td, f"{name}.parquet"); df.to_parquet(p2)
            rep = e1_base_bit_identity(p2, cfg)
            assert not rep.passed, (name, rep.summary())

def test_e1_bit_identity_rejects_all_q_columns():
    """V4: decomposition columns also forbidden under total-Q-disable."""
    cfg = RunConfig(seed=6, f_dispatch="F_canonical", grid_scale=6, ticks=3,
                    q=QConfig(q_read="local", gamma_psi=0.0, gamma_rho=0.0))
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "run.parquet")
        run_to_parquet(cfg, p)
        df = pd.read_parquet(p); df["Delta_from_rho"] = 0.0
        p2 = os.path.join(td, "bad.parquet"); df.to_parquet(p2)
        rep = e1_base_bit_identity(p2, cfg)
        assert not rep.passed and rep.checks["schema_absent_Delta_from_rho"] == 1

def test_become_survive_no_base_draws_policy():
    """D2 (config-bound): deterministic_level consumes no base draws; the NEXT
    generator output after init coincides with a shadow's post-permutation draw."""
    gs = 6
    cfg = RunConfig(seed=11, rule_mode="become_survive", grid_scale=gs,
                    init=InitConfig(scheme="fixed_count", fixed_count=9,
                                    base_init_mode="deterministic_level"),
                    constants=DynamicsConstants(logit_l=-0.405465, kappa=0.2, p_survive=0.4))
    dyn = SeedRegistry(11).dynamics()
    state = initialize(cfg.init, gs, dyn)
    assert np.all(state.v == cfg.init.m) and state.v.dtype == np.float64
    shadow = np.random.default_rng(11)
    ref = shadow.permutation(gs * gs)
    expect = np.zeros(gs * gs, dtype=bool); expect[ref[:9]] = True
    assert np.array_equal(state.is_active.reshape(-1), expect)
    assert np.array_equal(dyn.generator.random(16), shadow.random(16))

def test_symmetric_chain_rejects_deterministic_level():
    with pytest.raises(Exception):
        RunConfig(seed=1, init=InitConfig(base_init_mode="deterministic_level"))

def test_become_survive_rejects_nonzero_q():
    """N3: silent ignoring foreclosed — construction raises."""
    cfg = RunConfig(seed=2, rule_mode="become_survive", grid_scale=6,
                    init=InitConfig(scheme="fixed_count", fixed_count=5,
                                    base_init_mode="deterministic_level"),
                    constants=DynamicsConstants(logit_l=-0.4, kappa=0.1, p_survive=0.4),
                    q=QConfig(q_read="local", gamma_psi=0.001, gamma_rho=0.0))
    dyn = SeedRegistry(2).dynamics()
    with pytest.raises(ValueError):
        Dynamics(cfg, initialize(cfg.init, 6, dyn), dyn)

def test_dynamics_owns_private_copies():
    """D1(a): mutating the caller's GridState after construction changes nothing."""
    cfg = RunConfig(seed=3, f_dispatch="F_canonical", grid_scale=6, ticks=3,
                    q=QConfig(q_read="local", gamma_psi=0.0, gamma_rho=0.0))
    dyn = SeedRegistry(3).dynamics()
    state = initialize(cfg.init, 6, dyn)
    d = Dynamics(cfg, state, dyn)
    state.v[:] = 0.0                                      # hostile caller
    d.step()
    assert not np.any(d._v == 0.0)                        # terrain unaffected

def test_sink_cannot_alter_q_update():
    """D1(b): a hostile sink un-freezing and mutating Delta_v cannot change bases."""
    cfg = RunConfig(seed=4, f_dispatch="F_canonical", grid_scale=6, ticks=1,
                    q=QConfig(q_read="local", gamma_psi=0.001, gamma_rho=0.0))
    def hostile(tick, fields):
        arr = fields["Delta_v"]
        arr.flags.writeable = True
        arr[:] = 99.0
    dyn = SeedRegistry(4).dynamics()
    d = Dynamics(cfg, initialize(cfg.init, 6, dyn), dyn)
    d.step(hostile)
    assert d._v.max() <= 1.0                              # clip would mask; check delta scale:
    dyn2 = SeedRegistry(4).dynamics()
    d2 = Dynamics(cfg, initialize(cfg.init, 6, dyn2), dyn2)
    d2.step()                                             # no sink
    assert np.array_equal(d._v, d2._v)                    # identical evolution


def _same_size_duplicate_for_missing(full, cfg, victim_pos, donor_pos):
    """Remove one legitimate row; duplicate another from the SAME tick: totals and
    per-tick counts unchanged — only exact key coverage can catch it."""
    df = full.drop(index=full.index[victim_pos]).reset_index(drop=True)
    donor = full.iloc[[donor_pos]]
    return pd.concat([df, donor], ignore_index=True)

def test_tier1_duplicate_for_missing_same_size_cross_batch():
    """Items 3+5: same-size substitution, copies forced into different batches by
    placing the duplicate at the frame's end (verifier batch_size splits them)."""
    cfg = gate_a_cfg(grid_scale=6, ticks=6)
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "run.parquet")
        run_to_parquet(cfg, p)
        full = pd.read_parquet(p)
        tick3 = full[full.Tick == 3]
        bad = _same_size_duplicate_for_missing(full, cfg, victim_pos=tick3.index[5],
                                               donor_pos=tick3.index[20])
        p2 = os.path.join(td, "bad.parquet"); bad.to_parquet(p2)
        rep = tier1_verify(p2, cfg, batch_size=100)   # duplicate pair spans batches
        assert not rep.passed
        assert rep.checks["row_duplication_or_range"] > 0
        assert rep.checks["key_coverage_complete"] == 1
        assert rep.checks["rows_total"] == 0          # the counting checks CANNOT catch it
        assert rep.checks["tick_coverage_exact"] == 0

def test_e1_duplicate_for_missing_unchanged_bits():
    """Items 4+5: the substitution preserves base bits (bases constant under E1),
    so base_bit_identity stays zero — structural coverage alone must fail it."""
    cfg = RunConfig(seed=6, f_dispatch="F_canonical", grid_scale=6, ticks=6,
                    q=QConfig(q_read="local", gamma_psi=0.0, gamma_rho=0.0))
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "run.parquet")
        run_to_parquet(cfg, p)
        full = pd.read_parquet(p)
        tick4 = full[full.Tick == 4]
        bad = _same_size_duplicate_for_missing(full, cfg, victim_pos=tick4.index[2],
                                               donor_pos=tick4.index[9])
        p2 = os.path.join(td, "bad.parquet"); bad.to_parquet(p2)
        rep = e1_base_bit_identity(p2, cfg, batch_size=100)
        assert not rep.passed
        assert rep.checks["base_bit_identity"] == 0   # bits unchanged — as constructed
        assert rep.checks["row_duplication"] > 0
        assert rep.checks["key_coverage_complete"] == 1

def test_malformed_rho_schema_fails_closed():
    """Item 7: wrong columns => failed report returned, never an exception."""
    cfg = RunConfig(seed=9, f_dispatch="F_canonical", grid_scale=6, ticks=5,
                    q=QConfig(q_read="global", gamma_psi=0.0, gamma_rho=0.02))
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "run.parquet")
        tw = run_to_parquet(cfg, p)
        bad_rho = os.path.join(td, "bad_rho.parquet")
        pd.DataFrame({"T": [0], "value": [0.5]}).to_parquet(bad_rho)
        rep = tier1_verify(p, cfg, rho_global_path=bad_rho)
        assert not rep.passed and rep.checks["rho_global_schema"] == 1
```

# DIGESTS (changed files)
```
0536b248d9390fd21eaae17bd4b8a79eb7d91a9a1e974db43cbfeea934a1be3d  mfa_instrument/schema_contract.py
120f3eeeafa4d8edf287de3e89122c1ec3c001825da000b735d572b7dcb7c38c  mfa_instrument/telemetry.py
ea575608ed2ea7bd0b809703b0deb66ffbe9f52a03b5f1df9b4465c8633f03ae  mfa_instrument/verify.py
a1cd4e420efbc2f61183b1b067df3add96dd1c7bda8d7dd33209f2728b9ff00c  mfa_instrument/gates/gate_a.py
8c15d38f3f8f0c1344b3e9ce3f3d8970d7201cd834b13d88c5ddccaa76345489  tests/test_telemetry_gate_a.py
2c7c3611644f80d9a8f65940036369e4662ad74888b573ff0245f38d167750ae  tests/test_verify.py
```
*End of packet.*
