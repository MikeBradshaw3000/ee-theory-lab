# Note to L2 — E1 Closure Repair Return (the one held item, nothing else)

**From:** L1, routed by Mike
**Register:** closed, minimal — exactly the local repair your closure-hold requested. Two files changed (`verify.py`, `tests/test_verify.py`), carried verbatim below; no other source touched; no opportunistic hardening.

## The repair (your §3, implemented)

`e1_base_bit_identity()` now validates **Agent_X and Agent_Y independently** (each in [0, grid_scale)), exactly as Tier 1 does: `xy_ok` computed per row; `coordinate_range` accumulated and recorded; `gvalid = in_range & xy_ok` gates the seen-ledger, the tick-0 baselines, and every identity-index operation — invalid rows contribute to a failed report and can never become baseline entries, alias legitimate keys, or cause an indexing exception. The global seen ledger is otherwise unchanged, per your instruction.

## The discriminating negatives (your §4, implemented)

- `test_e1_alias_coordinate_rejected`: plants **(-1, 6) on a 6×6 grid** — flattened key 0, aliasing legal (0, 0) — with total and per-tick row counts preserved; asserts `rows_total` and `tick_coverage_exact` stay clean (the counting checks provably cannot catch it) while `coordinate_range == 1` and `key_coverage_complete == 1` (the displaced cell (3,2,4) uncovered) fail the file.
- `test_e1_gross_coordinate_fails_closed`: plants Agent_X = 9999, Agent_Y = −777, and an out-of-range tick; asserts the verifier returns a **failed report without raising** and `coordinate_range ≥ 2`.

## Suite

**70/70** (68 + the two negatives). Changed-file digests:
```
36f688aaaf6dbdde1cbe5e1b41a87eaed8494d18ca5cd374b12da03a75f27008  mfa_instrument/verify.py
28f9e5a6574ae05a21427eb2e89debbcb1a260c6c2a67fb669a32212dbd4100e  tests/test_verify.py
```

Requesting the closure disposition per your §6.

---

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
    coord_bad = 0        # closure repair: independent Agent_X/Agent_Y validation
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
        xs = df["Agent_X"].to_numpy(np.int64)
        ys = df["Agent_Y"].to_numpy(np.int64)
        # Closure repair (L2 held-item): validate BOTH coordinates independently —
        # a flattened key in [0, n_cells) does not prove its sources were in range
        # ((-1, 6) aliases (0, 0) on a 6x6 grid). Tier 1's discipline, applied here.
        xy_ok = ((xs >= 0) & (xs < cfg.grid_scale)
                 & (ys >= 0) & (ys < cfg.grid_scale))
        coord_bad += int((~xy_ok).sum())
        keys = xs * cfg.grid_scale + ys
        gkey = ticks.astype(np.int64) * n_cells + keys
        gvalid = in_range & xy_ok
        dup_bad += int(seen[gkey[gvalid]].sum())
        seen[gkey[gvalid]] = True
        bv = df["b_i_v"].to_numpy(np.float64).view(np.uint64)
        bu = df["b_i_u"].to_numpy(np.float64).view(np.uint64)
        br = df["b_i_r"].to_numpy(np.float64).view(np.uint64)
        valid_arr = gvalid
        for i in range(len(df)):
            if not valid_arr[i]:
                continue          # invalid rows fail via coordinate_range/coverage,
                                  # never enter baselines, never index out of range
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
    rep.record("coordinate_range", coord_bad)          # closure repair
    rep.record("row_duplication", dup_bad)                              # item 4
    rep.record("key_coverage_complete", 0 if bool(seen.all()) else 1)   # item 4
    return rep
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


def test_e1_alias_coordinate_rejected():
    """Closure negative (L2 held-item): (-1, 6) on a 6x6 grid flattens to key 0,
    aliasing legal (0,0). Row and per-tick counts are preserved, so only independent
    coordinate validation (and the resulting key-coverage gap) can fail the file."""
    cfg = RunConfig(seed=6, f_dispatch="F_canonical", grid_scale=6, ticks=6,
                    q=QConfig(q_read="local", gamma_psi=0.0, gamma_rho=0.0))
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "run.parquet")
        run_to_parquet(cfg, p)
        df = pd.read_parquet(p)
        idx = df[(df.Tick == 3) & (df.Agent_X == 2) & (df.Agent_Y == 4)].index[0]
        df.loc[idx, "Agent_X"] = -1
        df.loc[idx, "Agent_Y"] = 6            # flattened: -1*6 + 6 = 0 => aliases (0,0)
        p2 = os.path.join(td, "alias.parquet"); df.to_parquet(p2)
        rep = e1_base_bit_identity(p2, cfg, batch_size=100)
        assert not rep.passed
        assert rep.checks["coordinate_range"] == 1
        assert rep.checks["key_coverage_complete"] == 1   # (3,2,4) now uncovered
        assert rep.checks["rows_total"] == 0              # counting checks cannot catch it
        assert rep.checks["tick_coverage_exact"] == 0

def test_e1_gross_coordinate_fails_closed():
    """Closure negative: grossly out-of-range coordinates yield a FAILED REPORT,
    never an indexing exception (fail-closed, matching the rho discipline)."""
    cfg = RunConfig(seed=6, f_dispatch="F_canonical", grid_scale=6, ticks=4,
                    q=QConfig(q_read="local", gamma_psi=0.0, gamma_rho=0.0))
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "run.parquet")
        run_to_parquet(cfg, p)
        df = pd.read_parquet(p)
        df.loc[df.index[7], "Agent_X"] = 9999
        df.loc[df.index[8], "Agent_Y"] = -777
        df.loc[df.index[9], "Tick"] = 10_000          # out-of-range tick too
        p2 = os.path.join(td, "gross.parquet"); df.to_parquet(p2)
        rep = e1_base_bit_identity(p2, cfg, batch_size=50)   # must not raise
        assert not rep.passed
        assert rep.checks["coordinate_range"] >= 2
```
*End of packet.*
