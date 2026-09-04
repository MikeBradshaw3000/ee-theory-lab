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
                              NOISE_COLUMN, RHO_TABLE_COLUMNS,
                              BECOME_SURVIVE_COLUMNS)
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
    rule_mode="become_survive" selects the Lineage B family (schema_contract
    .BECOME_SURVIVE_COLUMNS) and REFUSES any Q coefficient or noise at construction:
    the writer-layer twin of the dynamics N3 refusal (Q-disabled subset only).
    """

    def __init__(self, grid_scale: int, gamma_psi: float, gamma_rho: float,
                 noise_enabled: bool, chunk_ticks: int = 500,
                 rule_mode: str = "symmetric_chain") -> None:
        if rule_mode not in ("symmetric_chain", "become_survive"):
            raise ValueError(f"unknown rule_mode {rule_mode!r}")
        if rule_mode == "become_survive":
            if gamma_psi != 0.0 or gamma_rho != 0.0:
                raise ValueError("become_survive telemetry supports the Q-disabled subset "
                                 "only (N3 ruling): gamma_psi and gamma_rho must be 0.0")
            if noise_enabled:
                raise ValueError("become_survive carries no noise channel: "
                                 "noise_enabled must be False")
        self.rule_mode = rule_mode
        self._gs = grid_scale
        xs, ys = np.indices((grid_scale, grid_scale))
        self._xs = xs.flatten()
        self._ys = ys.flatten()
        self._gamma_psi = gamma_psi
        if rule_mode == "become_survive":
            cols = list(BECOME_SURVIVE_COLUMNS)
        else:
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
    B_SINK_FIELDS = frozenset(c for c in BECOME_SURVIVE_COLUMNS
                              if c not in ("Tick", "Agent_X", "Agent_Y"))

    def sink(self, tick: int, fields: Dict[str, np.ndarray]) -> None:
        if self.rule_mode == "become_survive":
            # Exact input family, fail closed (L2 item-4 T1): extras — including
            # A-family names and rho_global (B tick-table emission is deferred by
            # the item boundary) — are rejected, never silently dropped or consumed.
            have = frozenset(fields)
            if have != self.B_SINK_FIELDS:
                raise ValueError(
                    "become_survive sink requires exactly the fields "
                    f"{sorted(self.B_SINK_FIELDS)}; missing={sorted(self.B_SINK_FIELDS - have)} "
                    f"extra={sorted(have - self.B_SINK_FIELDS)}")
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
