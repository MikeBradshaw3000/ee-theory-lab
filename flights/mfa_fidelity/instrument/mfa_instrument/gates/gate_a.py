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
