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
