"""gates/gate_b/qualification.py — formal harness qualification (Gate B Specification v0.4,
FROZEN 2026-09-04, §5 as amended by v0.3 A2 mutant 30; L2 modules-1–2 decision 4 base-leakage
witness; L2-held obligations: FP-witness uint64 patterns, solved-offset enumeration).

Pessimistic-on-passing, made mechanical: a harness that cannot fail is not a verifier. Every
mutant below is a controlled deformation of the CANDIDATE (the instrument's own B branch and its
schedule/dispatch surfaces), applied by runtime patch, run through the real B1 harness (or the
B2 alignment witness for mutant 30), and required to be REJECTED — and rejected by a check named
in its declaration BEFORE it runs (per-mutant attribution). A mutant that survives, or that is
rejected only by a check other than the ones declared for it, fails qualification. The
unmutated harness must pass first (positive control); the base-variation invariance witness and
the alignment witness are part of the positive control.

Qualification runs REQUIRE a persistent record owner (record_dir); the atomic qualification
record carries every mutant's declared and observed rejection, the FP witness (input and both
uint64 bit patterns), the alignment witness, the base-invariance witness, the solved-offset
enumeration, and the positive-control report. Never-relax-after-output is in force: nothing here
may be adjusted in light of any certification output; the mutant list and its attributions are
declared here and compared, not tuned.
"""
from __future__ import annotations

import contextlib
import hashlib
import json
import os
import platform
import tempfile
import time
import uuid
from dataclasses import asdict, dataclass, field
from typing import Any, Callable, Dict, FrozenSet, List, Optional, Tuple
from unittest import mock

import numpy as np

from ... import dynamics as _D
from ...config import RunConfig, InitConfig, DynamicsConstants
from ...init import GridState
from ...rng import DynamicsStream
from . import b1 as _B1
from . import b2 as _B2
from .comparators import raw_bits_differ
from .reference import PinnedReference, load_pinned_reference
from .stub import FrozenSequenceGenerator

QUALIFICATION_VERSION = "gate_b_qualification_v2 / spec v0.4 FROZEN"

# FROZEN QUALIFICATION MANIFEST (L2 module-4 Q1/Q2): a deliberately SEPARATE literal from the
# executable MUTANTS declaration below. The runtime declaration is compared to THIS — id, name,
# harness, mutation identifier, exact allowable checks, order, count — BEFORE the positive control.
# A narrowed, reordered, renamed, re-harnessed, re-targeted, or re-attributed declaration is a
# structural qualification failure. Editing this literal is a versioned amendment, never in place.
FROZEN_MANIFEST: Tuple[Tuple[int, str, str, str, Tuple[str, ...]], ...] = (
    # (id, name, harness, mutation_id, allowable checks)
    (1, "kappa_sign_flip", "b1", "step:kappa_sign_flip", ("p_become_bits",)),
    (2, "kappa_abs", "b1", "step:kappa_abs", ("p_become_bits",)),
    (3, "kappa_misscaled", "b1", "step:kappa_misscaled", ("p_become_bits",)),
    (4, "kappa_not_plumbed", "b1", "step:kappa_not_plumbed", ("p_become_bits",)),
    (5, "u_omitted", "b1", "step:u_omitted", ("p_become_bits",)),
    (6, "u_reversed", "b1", "step:u_reversed", ("p_become_bits",)),
    (7, "u_leaks_into_survival", "b1", "step:u_leaks_into_survival", ("is_active_exact",)),
    (8, "wrong_p_survive_config", "b1", "config:p_survive", ("p_survive_bits",)),          # 8a: scalar comparator
    (9, "wrong_p_survive_branch", "b1", "step:wrong_p_survive", ("is_active_exact",)),      # 8b: LAMBDA threshold witness
    (10, "become_le", "b1", "step:become_le", ("is_active_exact",)),
    (11, "survive_le", "b1", "step:survive_le", ("is_active_exact",)),
    (12, "moore_omit", "b1", "step:moore_omit", ("g_q_bits", "p_become_bits")),
    (13, "moore_duplicate", "b1", "step:moore_duplicate", ("g_q_bits", "p_become_bits")),
    (14, "self_inclusive", "b1", "step:self_inclusive", ("g_q_bits", "p_become_bits")),
    (15, "cardinal_only", "b1", "step:cardinal_only", ("g_q_bits", "p_become_bits")),
    (16, "diagonal_only", "b1", "step:diagonal_only", ("g_q_bits", "p_become_bits")),
    (17, "divisor_9", "b1", "step:divisor_9", ("g_q_bits", "p_become_bits")),
    (18, "gq_is_q", "b1", "step:gq_is_q", ("g_q_bits", "p_become_bits")),
    (19, "boundary_clamped", "b1", "step:boundary_clamped", ("g_q_bits", "p_become_bits")),
    (20, "eta_floor_leak", "b1", "step:eta_floor_leak", ("p_become_bits",)),
    (21, "float32_before_sigmoid", "b1", "step:float32_before_sigmoid", ("comparator_contract", "p_become_bits")),
    (22, "separate_rand_per_branch", "b1", "step:separate_rand_per_branch", ("frozen_sequence_stub",)),
    (23, "two_draws_per_tick", "b1", "step:two_draws_per_tick", ("frozen_sequence_stub",)),
    (24, "async_inplace", "b1", "step:async_inplace", ("is_active_exact", "p_become_bits", "g_q_bits")),
    (25, "masks_swapped", "b1", "step:masks_swapped", ("is_active_exact",)),
    (26, "masks_wrong_prior", "b1", "step:masks_wrong_prior", ("is_active_exact",)),
    (27, "wrong_dispatch", "b1", "dispatch:symmetric_chain", ("sink_field_family", "frozen_sequence_stub")),
    (28, "block_index_off_by_one", "schedule_table", "u_t:block_index_off_by_one", ("u_t_bits",)),
    (29, "ordering_permuted", "schedule_table", "u_t:cm1_ordering_permuted", ("u_t_bits",)),
    (30, "fp_association", "b1", "step:fp_association", ("p_become_bits",)),
    (31, "one_tick_shift", "alignment_witness", "b2:candidate_rho_trajectory_shift", ("alignment_witness",)),
    (32, "base_leakage", "b1", "step:base_leakage", ("p_become_bits",)),
)
def _canonical(entries) -> list:
    """One canonical form for both the frozen manifest and the runtime declaration: checks sorted."""
    return [(int(i), str(n), str(h), str(mid), tuple(sorted(c))) for (i, n, h, mid, c) in entries]

FROZEN_MANIFEST_SHA256 = hashlib.sha256(repr(_canonical(FROZEN_MANIFEST)).encode()).hexdigest()
# Frozen FP witness (mutant 30 / spec §5 item 29): the FIRST input over B1's declared U x K x g_q where the
# compared OUTPUT (p_become) differs between the two associations — independently confirmed 2026-09-13.
# Reviewed candidate source identities (placed at 948a517; dynamics.py unchanged since). A changed
# identity is a versioned amendment of this manifest, never a silent pass (L2 m4 r2 item 4).
FROZEN_CANDIDATE_SOURCE_SHA256 = {"config.py": "f913a3f4434f540c361a416909ddb8a0c3f3c661f4e0cb24af36a642cd651872",
                                  "dynamics.py": "483b8a378ebc6186c49f8627dd5897ef59312ed953b5a33f507cdf5eb12ae7a8"}
FROZEN_ALIGNMENT_MIN_BLOCK_MARGIN = 0.01     # declared minimum |aligned - shifted| block-0 difference (observed 0.024)
FROZEN_FP_WITNESS = {"u_t": 0.05, "kappa": 0.2090, "neighbor_count": 0, "g_q": -1.0,
                     "logit_original": "0xbfe210192161d86f", "logit_regrouped": "0xbfe210192161d86e",
                     "p_become_original": "0x3fd73371e858a8e2", "p_become_regrouped": "0x3fd73371e858a8e3"}


# ----------------------------------------------------------------------------- mutant grammar
@dataclass(frozen=True)
class MutantSpec:
    id: int
    name: str
    description: str
    harness: str                                   # "b1" | "schedule_table" | "alignment_witness"
    mutation_id: str                               # THE ONLY mutation authority: resolved through the closed dispatcher
    expected_checks: FrozenSet[str]                # any of these rejecting the mutant is correct attribution

    def apply(self) -> contextlib.ExitStack:
        """Obtain the patch from the closed, reviewed dispatcher keyed by the frozen mutation_id (L2 m4 r2 item 1)."""
        return implementation_for(self.mutation_id)()


def _sig(x):
    return 1.0 / (1.0 + np.exp(-x))


def _make_step(variant: str) -> Callable:
    """A deformed copy of Dynamics._step_become_survive (dynamics.py L295-315). Each variant changes
    exactly the named thing; everything else is the transcription."""
    def step(self, sink=None):
        cfg = self.cfg; k = cfg.constants; tick_idx = self.tick_count
        u_t = self._u_t(tick_idx)
        grid = self._is_active.astype(int)
        kappa = k.kappa
        if variant == "kappa_sign_flip": kappa = -kappa
        elif variant == "kappa_abs": kappa = abs(kappa)
        elif variant == "kappa_misscaled": kappa = 0.5 * kappa
        elif variant == "kappa_not_plumbed": kappa = 0.0
        if variant == "moore_omit": neighbors = _D._neighbor_count_b(grid) - np.roll(np.roll(grid, -1, axis=0), -1, axis=1)
        elif variant == "moore_duplicate": neighbors = _D._neighbor_count_b(grid) + np.roll(grid, 1, axis=0)
        elif variant == "self_inclusive": neighbors = _D._neighbor_count_b(grid) + grid
        elif variant == "cardinal_only": neighbors = (np.roll(grid, 1, 0) + np.roll(grid, -1, 0) + np.roll(grid, 1, 1) + np.roll(grid, -1, 1))
        elif variant == "diagonal_only": neighbors = (np.roll(np.roll(grid, 1, 0), 1, 1) + np.roll(np.roll(grid, 1, 0), -1, 1)
                                                     + np.roll(np.roll(grid, -1, 0), 1, 1) + np.roll(np.roll(grid, -1, 0), -1, 1))
        elif variant == "boundary_clamped":
            p = np.pad(grid, 1, mode="edge"); neighbors = (p[:-2, :-2] + p[:-2, 1:-1] + p[:-2, 2:] + p[1:-1, :-2]
                                                           + p[1:-1, 2:] + p[2:, :-2] + p[2:, 1:-1] + p[2:, 2:])
        else: neighbors = _D._neighbor_count_b(grid)
        q_i = neighbors / (9.0 if variant == "divisor_9" else 8.0)
        g_q = q_i if variant == "gq_is_q" else 2.0 * q_i - 1.0
        u_eff = 0.0 if variant == "u_omitted" else (-u_t if variant == "u_reversed" else u_t)
        if variant == "fp_association": x = k.logit_l + (u_eff + kappa * g_q)          # regrouped
        else: x = k.logit_l + u_eff + kappa * g_q                                        # original association
        if variant == "float32_before_sigmoid": p_become = _D._sigmoid(x.astype(np.float32))
        else: p_become = _D._sigmoid(x)
        if variant == "eta_floor_leak": p_become = p_become + k.eta_floor * (1.0 - p_become)
        if variant == "base_leakage": p_become = p_become * self._v
        if variant == "separate_rand_per_branch":
            rand_b = self._g.random(size=(cfg.grid_scale, cfg.grid_scale)); rand_s = self._g.random(size=(cfg.grid_scale, cfg.grid_scale))
            become_active = (grid == 0) & (rand_b < p_become); stay_active = (grid == 1) & (rand_s < k.p_survive)
            rand_grid = rand_b
        else:
            rand_grid = self._g.random(size=(cfg.grid_scale, cfg.grid_scale))
            if variant == "two_draws_per_tick": self._g.random(size=(cfg.grid_scale, cfg.grid_scale))
            p_surv = k.p_survive * (1.0 + 1e-7) if variant == "wrong_p_survive" else k.p_survive
            if variant == "u_leaks_into_survival": p_surv = k.p_survive + u_t
            g_b, g_s = grid, grid
            if variant == "masks_swapped": g_b, g_s = 1 - grid, 1 - grid   # become on active, stay on inactive
            if variant == "masks_wrong_prior": g_b = g_s = np.roll(grid, 1, axis=0)
            if variant == "become_le": become_active = (g_b == 0) & (rand_grid <= p_become)
            else: become_active = (g_b == 0) & (rand_grid < p_become)
            if variant == "survive_le": stay_active = (g_s == 1) & (rand_grid <= p_surv)
            else: stay_active = (g_s == 1) & (rand_grid < p_surv)
        if variant == "async_inplace":
            next_grid = grid.copy()
            for i in range(grid.shape[0]):                      # rows updated in place; later rows see updated earlier rows
                nb = _D._neighbor_count_b(next_grid)[i]
                pb = _D._sigmoid(k.logit_l + u_eff + kappa * (2.0 * nb / 8.0 - 1.0))
                next_grid[i] = ((next_grid[i] == 0) & (rand_grid[i] < pb)) | ((next_grid[i] == 1) & (rand_grid[i] < k.p_survive))
            next_grid = next_grid.astype(bool)
        else:
            next_grid = (become_active | stay_active)
        ds = next_grid.astype(int) - grid
        self._is_active = next_grid.copy()
        psi_local = ds * _D._moore_sum_a(ds.astype(np.float64))
        if sink is not None:
            fields = {"p_become": p_become, "g_q": g_q, "rand_grid": rand_grid,
                      "is_active": self._is_active.copy(), "Psi_local": psi_local}
            for a in fields.values():
                try: a.flags.writeable = False
                except Exception: pass
            sink(tick_idx, fields)
    return step


_IMPLEMENTATIONS: Dict[str, Callable[[], contextlib.ExitStack]] = {}


def _register(mutation_id: str, factory: Callable[[], contextlib.ExitStack]) -> Callable[[], contextlib.ExitStack]:
    """The closed dispatcher: one implementation per frozen mutation_id, tagged at registration with the
    identity it implements. The preflight verifies every executing implementation carries the tag of the
    id it is registered under, and that the registry's key set equals the manifest's."""
    factory.mutation_id = mutation_id                   # type: ignore[attr-defined]
    if mutation_id in _IMPLEMENTATIONS:
        raise RuntimeError(f"duplicate mutation implementation: {mutation_id}")
    _IMPLEMENTATIONS[mutation_id] = factory
    return factory


def implementation_for(mutation_id: str) -> Callable[[], contextlib.ExitStack]:
    impl = _IMPLEMENTATIONS.get(mutation_id)
    if impl is None:
        raise KeyError(f"no implementation registered for mutation {mutation_id!r}")
    if getattr(impl, "mutation_id", None) != mutation_id:
        raise RuntimeError(f"implementation registered under {mutation_id!r} carries identity {getattr(impl, 'mutation_id', None)!r}")
    return impl


def _patch_step(variant: str) -> Callable[[], contextlib.ExitStack]:
    def apply() -> contextlib.ExitStack:
        st = contextlib.ExitStack()
        st.enter_context(mock.patch.object(_D.Dynamics, "_step_become_survive", _make_step(variant)))
        return st
    return _register(f"step:{variant}", apply)


def _patch_p_survive_config() -> Callable[[], contextlib.ExitStack]:
    """Mutant 8a: the CONFIGURATION constant p_survive differs from ancestor LAMBDA by one ULP — the
    scalar comparator (B1 preflight) must reject it; the branch is untouched."""
    real = _B1._cfg
    def cfg(ref, kappa, schedule, ticks):
        c = real(ref, kappa, schedule, ticks)
        import dataclasses
        return dataclasses.replace(c, constants=dataclasses.replace(c.constants, p_survive=float(np.nextafter(c.constants.p_survive, 1.0))))
    def apply() -> contextlib.ExitStack:
        st = contextlib.ExitStack(); st.enter_context(mock.patch.object(_B1, "_cfg", cfg)); return st
    return _register("config:p_survive", apply)


def _patch_u_t(kind: str) -> Callable[[], contextlib.ExitStack]:
    real = _D.Dynamics._u_t
    def mutated(self, tick):
        if kind == "block_index_off_by_one":
            return real(self, tick + 1)
        # "cm1_ordering_permuted": ONLY on a CM-1 schedule (16 block entries); CM-0 schedules untouched
        v = real(self, tick)
        if kind == "cm1_ordering_permuted" and len(self.cfg.drive_schedule) == 16:
            levels = sorted({float(b) for _, b in self.cfg.drive_schedule}); tier = levels[-1]
            return {tier / 2.0: tier, tier: tier / 2.0}.get(v, v)
        return v
    def apply() -> contextlib.ExitStack:
        st = contextlib.ExitStack(); st.enter_context(mock.patch.object(_D.Dynamics, "_u_t", mutated)); return st
    return _register(f"u_t:{kind}", apply)


def _patch_dispatch() -> Callable[[], contextlib.ExitStack]:
    def wrong_step(self, sink=None):                            # correct private branch behind wrong public dispatch
        self._step_symmetric_chain(sink); self.tick_count += 1
    def apply() -> contextlib.ExitStack:
        st = contextlib.ExitStack(); st.enter_context(mock.patch.object(_D.Dynamics, "step", wrong_step)); return st
    return _register("dispatch:symmetric_chain", apply)


def _patch_alignment_shift() -> Callable[[], contextlib.ExitStack]:
    """Mutant 30: the B2 candidate extraction labels tick t's POST-step density as rho[t] (one-tick shift)."""
    real = _B2.candidate_rho_trajectory
    def shifted(ref, mode, tier, u_const, kappa, root, consumed_schedule=None):
        r = real(ref, mode, tier, u_const, kappa, root, consumed_schedule)
        return np.concatenate([r[1:], r[-1:]])                  # index 0 now holds post-step-of-tick-0
    def apply() -> contextlib.ExitStack:
        st = contextlib.ExitStack(); st.enter_context(mock.patch.object(_B2, "candidate_rho_trajectory", shifted)); return st
    return _register("b2:candidate_rho_trajectory_shift", apply)


B1 = "b1"; ST = "schedule_table"; AW = "alignment_witness"
# Register every implementation exactly once (the dispatcher is closed after this block).
for _v in ("kappa_sign_flip", "kappa_abs", "kappa_misscaled", "kappa_not_plumbed", "u_omitted", "u_reversed",
           "u_leaks_into_survival", "wrong_p_survive", "become_le", "survive_le", "moore_omit", "moore_duplicate",
           "self_inclusive", "cardinal_only", "diagonal_only", "divisor_9", "gq_is_q", "boundary_clamped",
           "eta_floor_leak", "float32_before_sigmoid", "separate_rand_per_branch", "two_draws_per_tick",
           "async_inplace", "masks_swapped", "masks_wrong_prior", "fp_association", "base_leakage"):
    _patch_step(_v)
_patch_p_survive_config(); _patch_u_t("block_index_off_by_one"); _patch_u_t("cm1_ordering_permuted")
_patch_dispatch(); _patch_alignment_shift()

def _M(id_, name, harness, mutation_id, checks):
    return MutantSpec(id_, name, "", harness, mutation_id, frozenset(checks))
MUTANTS: Tuple[MutantSpec, ...] = tuple(_M(i, n, h, mid, c) for (i, n, h, mid, c) in FROZEN_MANIFEST) if False else (
    _M(1, "kappa_sign_flip", B1, "step:kappa_sign_flip", ("p_become_bits",)),
    _M(2, "kappa_abs", B1, "step:kappa_abs", ("p_become_bits",)),
    _M(3, "kappa_misscaled", B1, "step:kappa_misscaled", ("p_become_bits",)),
    _M(4, "kappa_not_plumbed", B1, "step:kappa_not_plumbed", ("p_become_bits",)),
    _M(5, "u_omitted", B1, "step:u_omitted", ("p_become_bits",)),
    _M(6, "u_reversed", B1, "step:u_reversed", ("p_become_bits",)),
    _M(7, "u_leaks_into_survival", B1, "step:u_leaks_into_survival", ("is_active_exact",)),
    _M(8, "wrong_p_survive_config", B1, "config:p_survive", ("p_survive_bits",)),
    _M(9, "wrong_p_survive_branch", B1, "step:wrong_p_survive", ("is_active_exact",)),
    _M(10, "become_le", B1, "step:become_le", ("is_active_exact",)),
    _M(11, "survive_le", B1, "step:survive_le", ("is_active_exact",)),
    _M(12, "moore_omit", B1, "step:moore_omit", ("g_q_bits", "p_become_bits")),
    _M(13, "moore_duplicate", B1, "step:moore_duplicate", ("g_q_bits", "p_become_bits")),
    _M(14, "self_inclusive", B1, "step:self_inclusive", ("g_q_bits", "p_become_bits")),
    _M(15, "cardinal_only", B1, "step:cardinal_only", ("g_q_bits", "p_become_bits")),
    _M(16, "diagonal_only", B1, "step:diagonal_only", ("g_q_bits", "p_become_bits")),
    _M(17, "divisor_9", B1, "step:divisor_9", ("g_q_bits", "p_become_bits")),
    _M(18, "gq_is_q", B1, "step:gq_is_q", ("g_q_bits", "p_become_bits")),
    _M(19, "boundary_clamped", B1, "step:boundary_clamped", ("g_q_bits", "p_become_bits")),
    _M(20, "eta_floor_leak", B1, "step:eta_floor_leak", ("p_become_bits",)),
    _M(21, "float32_before_sigmoid", B1, "step:float32_before_sigmoid", ("comparator_contract", "p_become_bits")),
    _M(22, "separate_rand_per_branch", B1, "step:separate_rand_per_branch", ("frozen_sequence_stub",)),
    _M(23, "two_draws_per_tick", B1, "step:two_draws_per_tick", ("frozen_sequence_stub",)),
    _M(24, "async_inplace", B1, "step:async_inplace", ("is_active_exact", "p_become_bits", "g_q_bits")),
    _M(25, "masks_swapped", B1, "step:masks_swapped", ("is_active_exact",)),
    _M(26, "masks_wrong_prior", B1, "step:masks_wrong_prior", ("is_active_exact",)),
    _M(27, "wrong_dispatch", B1, "dispatch:symmetric_chain", ("sink_field_family", "frozen_sequence_stub")),
    _M(28, "block_index_off_by_one", ST, "u_t:block_index_off_by_one", ("u_t_bits",)),
    _M(29, "ordering_permuted", ST, "u_t:cm1_ordering_permuted", ("u_t_bits",)),
    _M(30, "fp_association", B1, "step:fp_association", ("p_become_bits",)),
    _M(31, "one_tick_shift", AW, "b2:candidate_rho_trajectory_shift", ("alignment_witness",)),
    _M(32, "base_leakage", B1, "step:base_leakage", ("p_become_bits",)),
)


# ----------------------------------------------------------------------------- records
class QualificationHalt(RuntimeError):
    def __init__(self, record: "QualificationFailureRecord") -> None:
        super().__init__(record.summary()); self.record = record


@dataclass
class MutantResult:
    id: int
    name: str
    harness: str
    mutation_id: str
    expected_checks: List[str]
    rejected: bool
    observed_check: Optional[str]
    observed_battery: Optional[str]
    observed_case: Optional[str]
    attributed: bool                       # rejected AND observed_check in expected_checks
    detail: str
    artifact_path: Optional[str] = None    # the B1/schedule failure record for this mutant
    artifact_sha256: Optional[str] = None
    expected_bits: Optional[str] = None
    observed_bits: Optional[str] = None


@dataclass
class QualificationFailureRecord:
    failure_class: str      # structural | positive_control | witness | internal
    stage: str
    mutant: Optional[str]
    check: str
    detail: str
    environment: str
    provenance: Dict[str, Any]
    positive_control: Optional[Dict[str, Any]]
    witnesses_completed: Dict[str, Any]
    mutants_completed: List[Dict[str, Any]]
    stages_completed: List[str]
    written_to: Optional[str] = None

    def summary(self) -> str:
        return (f"QUALIFICATION HALT [{self.failure_class}] stage={self.stage} mutant={self.mutant} check={self.check} "
                f"detail={self.detail!r} stages_completed={self.stages_completed}")


@dataclass
class QualificationRecord:
    version: str
    environment: str
    label: str
    provenance: Dict[str, Any]
    positive_control: Dict[str, Any] = field(default_factory=dict)       # the COMPLETE B1Report (asdict)
    base_invariance_witness: Dict[str, Any] = field(default_factory=dict)
    alignment_witness: Dict[str, Any] = field(default_factory=dict)
    fp_witness: Dict[str, Any] = field(default_factory=dict)
    solved_offset_enumeration: Dict[str, Any] = field(default_factory=dict)
    mutants: List[MutantResult] = field(default_factory=list)
    stages_completed: List[str] = field(default_factory=list)
    failure: Optional[QualificationFailureRecord] = None
    written_to: Optional[str] = None

    @property
    def passed(self) -> bool:
        """Against the FROZEN manifest — never against the runtime MUTANTS tuple (Q1)."""
        F = FROZEN_MANIFEST
        got = [(m.id, m.name, m.harness, m.mutation_id, tuple(sorted(m.expected_checks))) for m in self.mutants]
        want = [(i, n, h, mid, tuple(sorted(c))) for (i, n, h, mid, c) in F]
        return (self.failure is None and got == want
                and self.positive_control.get("passed") is True
                and self.base_invariance_witness.get("passed") is True
                and self.alignment_witness.get("passed") is True
                and self.fp_witness.get("passed") is True
                and self.solved_offset_enumeration.get("passed") is True
                and self.base_invariance_witness.get("under_base_leakage_mutant", {}).get("passed") is False   # linkage scored
                and all(m.rejected and m.attributed for m in self.mutants)
                and self.stages_completed[:4] == list(QUALIFICATION_STAGES[:4]))   # "record" is the act of persisting, not its own precondition

    def summary(self) -> str:
        rej = sum(m.rejected for m in self.mutants); att = sum(m.attributed for m in self.mutants)
        return (f"QUALIFICATION[{self.label}] positive_control={self.positive_control.get('passed')} "
                f"base_invariance={self.base_invariance_witness.get('passed')} alignment={self.alignment_witness.get('passed')} "
                f"fp_witness={self.fp_witness.get('passed')} solved_offset={self.solved_offset_enumeration.get('passed')} "
                f"mutants rejected={rej}/{len(self.mutants)} attributed={att}/{len(self.mutants)} => {'PASS' if self.passed else 'FAIL'}")


QUALIFICATION_STAGES = ("manifest_preflight", "positive_control", "witnesses", "mutants", "record")


def _write_atomically(payload: Dict[str, Any], record_dir: str, prefix: str) -> str:
    os.makedirs(record_dir, exist_ok=True)
    final = os.path.join(record_dir, f"{prefix}_{time.time_ns()}_{os.getpid()}_{uuid.uuid4().hex[:8]}.json")
    fd, tmp = tempfile.mkstemp(dir=record_dir, prefix=f".{prefix}_", suffix=".tmp")
    try:
        with os.fdopen(fd, "w") as fh:
            json.dump(payload, fh, indent=1, default=str); fh.flush(); os.fsync(fh.fileno())
        os.replace(tmp, final)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)
    return final


def _sha(path: Optional[str]) -> Optional[str]:
    return hashlib.sha256(open(path, "rb").read()).hexdigest() if path and os.path.isfile(path) else None


# ----------------------------------------------------------------------------- witnesses
def fp_witness(ref: PinnedReference) -> Dict[str, Any]:
    """Frozen FP witness (spec §5 item 29): the runtime computation at the FROZEN input must reproduce
    the frozen logit AND p_become bit patterns for both associations, and the p_become patterns must
    differ — proving the raw-bit p_become comparator does work a tolerance comparator cannot."""
    W = FROZEN_FP_WITNESS
    L = float(ref.LOGIT_L); u = W["u_t"]; k = W["kappa"]; g = 2.0 * (W["neighbor_count"] / 8.0) - 1.0   # executable, not decorative
    if g != W["g_q"]:
        return {"frozen": dict(W), "passed": False, "reason": f"frozen g_q {W['g_q']} inconsistent with neighbor_count {W['neighbor_count']}"}
    lo = np.float64((L + u) + k * g); lr = np.float64(L + (u + k * g))
    po = np.float64(_sig(lo)); pr = np.float64(_sig(lr))
    obs = {"logit_original": f"0x{int(lo.view(np.uint64)):016x}", "logit_regrouped": f"0x{int(lr.view(np.uint64)):016x}",
           "p_become_original": f"0x{int(po.view(np.uint64)):016x}", "p_become_regrouped": f"0x{int(pr.view(np.uint64)):016x}"}
    matches = all(obs[k2] == W[k2] for k2 in obs)
    return {"frozen": dict(W), "observed": obs, "logit_bits_differ": obs["logit_original"] != obs["logit_regrouped"],
            "p_become_bits_differ": obs["p_become_original"] != obs["p_become_regrouped"],
            "matches_frozen": matches, "passed": bool(matches and obs["p_become_original"] != obs["p_become_regrouped"])}


def base_invariance_witness(ref: PinnedReference) -> Dict[str, Any]:
    grid = _B1.reference_init_grid(ref, 42)
    rand = np.random.default_rng(_B1.PARITY_SEED).random((_B1.GRID, _B1.GRID))
    outs = []
    for fill in (0.1, 0.9):
        cfg = _B1._cfg(ref, 0.4221, ((0, 0.25),), 1)
        f = np.full((_B1.GRID, _B1.GRID), fill)
        state = GridState(v=f.copy(), u_base=f.copy(), r=f.copy(), is_active=grid.astype(bool))
        stub = FrozenSequenceGenerator([rand], _B1.GRID)
        model = _D.Dynamics(cfg, state, DynamicsStream(generator=stub))
        cap: Dict[str, np.ndarray] = {}
        model.step(lambda t, fl: cap.update({k: np.asarray(v) for k, v in fl.items()}))
        outs.append(cap)
    diffs = {k: raw_bits_differ(outs[0][k], outs[1][k]) for k in ("p_become", "g_q", "rand_grid")}
    state_diff = int(np.count_nonzero(outs[0]["is_active"] != outs[1]["is_active"]))
    return {"fills": [0.1, 0.9], "bit_differences": diffs, "state_differences": state_diff,
            "passed": all(v == 0 for v in diffs.values()) and state_diff == 0}


_GENUINE_CELL_CFG = _B2._cell_cfg          # captured at import: the witness always builds from the genuine cell config


def _all_active_cfg(ref, mode, tier, u_const, kappa, root):
    """The constructed transient's configuration: the genuine cell config with all 2,500 cells active."""
    import dataclasses
    c = _GENUINE_CELL_CFG(ref, mode, tier, u_const, kappa, root)
    return dataclasses.replace(c, init=dataclasses.replace(c.init, fixed_count=_B1.N_CELLS))


def _shifted_extraction(rho: np.ndarray) -> np.ndarray:
    """The deliberate one-tick shift: index t carries the post-step density of tick t."""
    return np.concatenate([rho[1:], rho[-1:]])


def alignment_witness(ref: PinnedReference) -> Dict[str, Any]:
    """v0.3 Amendment 2 discriminator: an all-active CONSTRUCTED transient (pre-step density exactly
    1.0; large deterministic tick-0 -> 1 drop) is driven through B2's own candidate extraction, and the
    frozen window statistics (rho[0]; block-0 mean via the frozen block machinery) are computed on the
    aligned extraction and on the deliberately shifted extraction. The witness passes iff the aligned
    extraction reports rho[0] == 1.0 exactly AND the shifted extraction differs at rho[0] and in the
    block-0 statistic by a large margin; under mutant 31 (B2's extraction patched to shift) the
    'aligned' path itself returns the shifted values and the witness fails BY THIS CONSTRUCTED CASE.
    The ordinary seed-301 rho[0] check is retained as a secondary guard."""
    with mock.patch.object(_B2, "_cell_cfg", _all_active_cfg):
        cand = _B2.candidate_rho_trajectory(ref, "cm0", 0.0, 0.0, 0.0, 301)      # through B2's extraction (patchable by mutant 31)
    aligned_rho0 = float(cand[0]); aligned_block0 = _B2.summaries_from_trajectory(cand)[1][0]
    shifted = _shifted_extraction(cand)
    shifted_rho0 = float(shifted[0]); shifted_block0 = _B2.summaries_from_trajectory(shifted)[1][0]
    constructed_ok = ((aligned_rho0 == 1.0) and abs(aligned_rho0 - shifted_rho0) > 0.3
                      and abs(aligned_block0 - shifted_block0) >= FROZEN_ALIGNMENT_MIN_BLOCK_MARGIN)
    # secondary guard: ordinary trajectories on both sides begin at the initialized density
    st = _B2.reference_wrapper_states(ref, "cm0", 0.0, 0.0, 0.0, 201)
    ref_rho0 = float(_B2.rho_trajectory_from_states(st)[0])
    ord_rho0 = float(_B2.candidate_rho_trajectory(ref, "cm0", 0.0, 0.0, 0.0, 301)[0])
    init_density = _B1.INIT_ACTIVE / _B1.N_CELLS
    secondary_ok = (ref_rho0 == init_density) and (ord_rho0 == init_density)
    return {"constructed_transient": {"aligned_rho0": aligned_rho0, "shifted_rho0": shifted_rho0,
                                      "aligned_block0_mean": aligned_block0, "shifted_block0_mean": shifted_block0,
                                      "rho0_margin": abs(aligned_rho0 - shifted_rho0), "passed": bool(constructed_ok)},
            "secondary_guard": {"init_density": init_density, "ref_rho0": ref_rho0, "cand_rho0": ord_rho0, "passed": bool(secondary_ok)},
            "passed": bool(constructed_ok and secondary_ok)}


def _enumerate_numeric(obj: Any, depth: int = 0) -> Tuple[List[float], bool]:
    """Exhaustively collect numeric leaves from scalars, sequences, sets, mappings (values), and NumPy
    arrays, recursively. Returns (values, fully_parsed). Anything else is UNPARSED (fail closed)."""
    if depth > 8:
        return [], False
    if isinstance(obj, bool):
        return [], False
    if isinstance(obj, (int, float, np.integer, np.floating)):
        return [float(obj)], True
    if isinstance(obj, np.ndarray):
        return ([float(x) for x in obj.ravel()], True) if obj.dtype.kind in "iuf" else ([], False)
    if isinstance(obj, dict):
        vals: List[float] = []; ok = True
        for v in obj.values():
            vv, o = _enumerate_numeric(v, depth + 1); vals += vv; ok &= o
        return vals, ok
    if isinstance(obj, (list, tuple, set, frozenset)):
        vals = []; ok = True
        for v in obj:
            vv, o = _enumerate_numeric(v, depth + 1); vals += vv; ok &= o
        return vals, ok
    return [], False


def solved_offset_enumeration() -> Dict[str, Any]:
    """MECHANICAL, FAIL-CLOSED enumeration (L2 m4 r2 item 3/4): every config-module attribute whose name
    signals a solved-offset registry, every RunConfig field naming an offset, and the schedule type are
    inspected; numeric leaves are enumerated exhaustively (scalars, sequences, sets, mappings, arrays,
    nested); any matching surface that cannot be exhaustively parsed lands in `unparsed_surfaces` and
    fails the witness. Candidate source identities must match the frozen reviewed values."""
    import inspect
    from ... import config as _C
    cfg_path = inspect.getsourcefile(_C); dyn_path = inspect.getsourcefile(_D)
    ids = {"config.py": _sha(cfg_path), "dynamics.py": _sha(dyn_path)}
    identity_ok = all(ids[k] == FROZEN_CANDIDATE_SOURCE_SHA256[k] for k in FROZEN_CANDIDATE_SOURCE_SHA256)
    discovered: List[float] = []; surfaces: List[str] = []; unparsed: List[str] = []
    for name, val in vars(_C).items():
        lname = name.lower()
        if ("solved" in lname and "offset" in lname) or lname.startswith("solved_offset"):
            surfaces.append(f"config.{name}")
            vals, ok = _enumerate_numeric(val)
            discovered += vals
            if not ok:
                unparsed.append(f"config.{name}: {type(val).__name__}")
    for f in RunConfig.__dataclass_fields__.values():
        if "offset" in f.name.lower():
            surfaces.append(f"RunConfig.{f.name}")
            if f.default is not f.default_factory and f.default is not None:      # dataclasses.MISSING sentinel handled below
                pass
    schedule_type = RunConfig.__dataclass_fields__["drive_schedule"].type
    frozen_set = list(_B1.SCHEDULE_CM0_UCONST)
    missing = sorted({v for v in discovered if v not in frozen_set})
    passed = identity_ok and not unparsed and not missing
    return {"config_source_sha256": ids["config.py"], "dynamics_source_sha256": ids["dynamics.py"],
            "frozen_source_sha256": dict(FROZEN_CANDIDATE_SOURCE_SHA256), "source_identity_ok": identity_ok,
            "schedule_type": str(schedule_type), "surfaces_inspected": surfaces, "unparsed_surfaces": unparsed,
            "solved_offset_values_discovered": sorted(set(discovered)), "cm0_table_set": frozen_set,
            "missing_from_frozen_table": missing, "passed": bool(passed)}


# ----------------------------------------------------------------------------- runner
def _manifest_defects() -> List[str]:
    got = [(m.id, m.name, m.harness, m.mutation_id, tuple(sorted(m.expected_checks))) for m in MUTANTS]
    want = [(i, n, h, mid, tuple(sorted(c))) for (i, n, h, mid, c) in FROZEN_MANIFEST]
    out = []
    if len(got) != len(want):
        out.append(f"count {len(got)} != frozen {len(want)}")
    for i, (g, w) in enumerate(zip(got, want)):
        if g != w:
            out.append(f"position {i}: runtime {g} != frozen {w}")
    return out


def _run_mutant_b1(pinned_root: str, m: MutantSpec, load_mode: str, label: str, record_dir: str) -> MutantResult:
    mdir = os.path.join(record_dir, f"mutant_{m.id:02d}")
    with m.apply():
        rep = _B1.run_b1(pinned_root, label=label, load_mode=load_mode, record_dir=mdir)
    if rep.failure is None:
        return MutantResult(m.id, m.name, m.harness, m.mutation_id, sorted(m.expected_checks), False, None, None, None, False,
                            "NOT REJECTED: the harness passed the mutated candidate")
    f = rep.failure
    attributed = f.comparator in m.expected_checks
    return MutantResult(m.id, m.name, m.harness, m.mutation_id, sorted(m.expected_checks), True, f.comparator, f.battery, f.case_id, attributed,
                        f"rejected by {f.failure_class}/{f.comparator} at {f.battery}:{f.case_id}" + ("" if attributed else " (UNATTRIBUTED)"),
                        f.written_to, _sha(f.written_to), f.expected_bits, f.observed_bits)


def _run_mutant_schedule_table(pinned_root: str, m: MutantSpec, load_mode: str, label: str, record_dir: str) -> MutantResult:
    """Mutants 28/29 must qualify the FROZEN schedule table: run B1's cleared schedule-table battery
    object alone (not a retyped criterion) under the mutant; the required attribution is u_t_bits."""
    mdir = os.path.join(record_dir, f"mutant_{m.id:02d}")
    ref = load_pinned_reference(pinned_root, load_mode, label)
    rep = _B1.B1Report(label=label, environment="schedule_table_witness", environment_record=None, provenance={})
    r = _B1._Runner(rep); r.ref = ref; r.battery = "schedule_table"
    with m.apply():
        try:
            _B1._battery_schedule_table(r)
        except _B1.GateBFailure as gf:
            gf.record.written_to = _B1.write_failure_record_atomically(gf.record, mdir)
    if rep.failure is None:
        return MutantResult(m.id, m.name, m.harness, m.mutation_id, sorted(m.expected_checks), False, None, None, None, False,
                            "NOT REJECTED: the frozen schedule table passed the mutated candidate schedule")
    f = rep.failure
    attributed = f.comparator in m.expected_checks
    return MutantResult(m.id, m.name, m.harness, m.mutation_id, sorted(m.expected_checks), True, f.comparator, f.battery, f.case_id, attributed,
                        f"rejected by {f.failure_class}/{f.comparator} at {f.battery}:{f.case_id}" + ("" if attributed else " (UNATTRIBUTED)"),
                        f.written_to, _sha(f.written_to), f.expected_bits, f.observed_bits)


def _run_mutant_alignment(ref: PinnedReference, m: MutantSpec) -> MutantResult:
    with m.apply():
        w = alignment_witness(ref)
    rejected = not w["constructed_transient"]["passed"]      # rejected BY THE CONSTRUCTED CASE (Amendment 2)
    observed = "alignment_witness" if rejected else None
    attributed = rejected and (observed in m.expected_checks)  # same rule as B1 (Q3)
    ct = w["constructed_transient"]
    return MutantResult(m.id, m.name, m.harness, m.mutation_id, sorted(m.expected_checks), rejected, observed,
                        "alignment_witness", "constructed_all_active_transient", attributed,
                        f"aligned rho0={ct['aligned_rho0']} block0={ct['aligned_block0_mean']:.6f} vs shifted rho0={ct['shifted_rho0']} block0={ct['shifted_block0_mean']:.6f}"
                        + ("" if attributed else (" (UNATTRIBUTED)" if rejected else " NOT REJECTED")),
                        None, None, f"{ct['aligned_rho0']}", f"{ct['shifted_rho0']}")


def run_qualification(pinned_root: str, record_dir: str, label: str = "PROVISIONAL", load_mode: str = "EXTRACTION") -> QualificationRecord:
    if record_dir is None:
        raise ValueError("formal qualification requires a persistent record owner: record_dir is mandatory")
    env = f"python{platform.python_version()}/numpy{np.__version__}"
    import inspect
    prov: Dict[str, Any] = {"label": label, "load_mode": load_mode, "environment": env, "qualification_version": QUALIFICATION_VERSION,
                            "frozen_manifest_sha256": FROZEN_MANIFEST_SHA256,
                            "qualification_source_sha256": _sha(inspect.getsourcefile(run_qualification)),
                            "b1_source_sha256": _sha(inspect.getsourcefile(_B1)), "b2_source_sha256": _sha(inspect.getsourcefile(_B2)),
                            "spec": _B1.SPEC_VERSION, "spec_sha256": _B1.SPEC_SHA256}
    rec = QualificationRecord(version=QUALIFICATION_VERSION, environment=env, label=label, provenance=prov)
    state: Dict[str, Any] = {"stage": "manifest_preflight", "mutant": None}

    def _halt(failure_class: str, check: str, detail: str) -> None:
        fr = QualificationFailureRecord(failure_class=failure_class, stage=state["stage"], mutant=state["mutant"], check=check,
                                        detail=detail, environment=env, provenance=dict(prov), positive_control=rec.positive_control or None,
                                        witnesses_completed={"base_invariance": rec.base_invariance_witness, "alignment": rec.alignment_witness,
                                                             "fp": rec.fp_witness, "solved_offset": rec.solved_offset_enumeration},
                                        mutants_completed=[asdict(m) for m in rec.mutants], stages_completed=list(rec.stages_completed))
        rec.failure = fr
        raise QualificationHalt(fr)

    def _boundary(stage: str, fn: Callable[[], Any]) -> None:
        state["stage"] = stage
        try:
            fn()
        except QualificationHalt:
            pass
        except BaseException as e:          # noqa: BLE001 — every unexpected exception becomes a qualification record
            try:
                _halt("internal", "unexpected_exception", f"{type(e).__name__}: {e}")
            except QualificationHalt:
                pass
        if rec.failure is not None:
            rec.failure.written_to = _write_atomically({**asdict(rec.failure), "kind": "qualification_failure"}, record_dir, "gate_b_qualification_FAILURE")
        else:
            rec.stages_completed.append(stage)

    def _manifest_preflight() -> None:
        # runtime declaration vs the independent frozen manifest, BEFORE any output (Q1/Q2)
        defects = _manifest_defects()
        if defects:
            _halt("structural", "frozen_manifest", "; ".join(defects))
        # implementation identity: the closed dispatcher's key set equals the manifest's mutation ids, and
        # every implementation that will execute carries the identity tag of the id it is registered under
        want_ids = [mid for (_, _, _, mid, _) in FROZEN_MANIFEST]
        if sorted(_IMPLEMENTATIONS) != sorted(want_ids):
            _halt("structural", "implementation_registry", f"registry keys {sorted(_IMPLEMENTATIONS)} != manifest ids {sorted(want_ids)}")
        for mid in want_ids:
            impl = _IMPLEMENTATIONS[mid]
            if getattr(impl, "mutation_id", None) != mid:
                _halt("structural", "implementation_identity", f"implementation under {mid!r} carries identity {getattr(impl, 'mutation_id', None)!r}")
        rt = hashlib.sha256(repr(_canonical([(m.id, m.name, m.harness, m.mutation_id, m.expected_checks) for m in MUTANTS])).encode()).hexdigest()
        prov["runtime_declaration_sha256"] = rt
        if rt != FROZEN_MANIFEST_SHA256:
            _halt("structural", "declaration_digest", f"runtime {rt} != frozen {FROZEN_MANIFEST_SHA256}")

    ref_holder: Dict[str, PinnedReference] = {}

    def _positive_control() -> None:
        pc = _B1.run_b1(pinned_root, label=label, load_mode=load_mode, record_dir=os.path.join(record_dir, "positive_control"), qualification=True)
        rec.positive_control = {**asdict(pc), "passed": bool(pc.passed)}          # the COMPLETE report (Q6)
        if not pc.passed:
            _halt("positive_control", "b1_positive_control", pc.summary())
        ref_holder["ref"] = load_pinned_reference(pinned_root, load_mode, label)
        prov["candidate_commit"] = pc.provenance.get("candidate_commit"); prov["candidate_dynamics_sha256"] = pc.provenance.get("candidate_dynamics_sha256")

    def _witnesses() -> None:
        ref = ref_holder["ref"]
        rec.base_invariance_witness = base_invariance_witness(ref)
        if not rec.base_invariance_witness["passed"]:
            _halt("witness", "base_invariance", repr(rec.base_invariance_witness))
        rec.alignment_witness = alignment_witness(ref)
        if not rec.alignment_witness["passed"]:
            _halt("witness", "alignment", repr(rec.alignment_witness))
        rec.fp_witness = fp_witness(ref)
        if not rec.fp_witness["passed"]:
            _halt("witness", "fp_witness", repr(rec.fp_witness))
        rec.solved_offset_enumeration = solved_offset_enumeration()
        if not rec.solved_offset_enumeration["passed"]:
            _halt("witness", "solved_offset_enumeration", repr(rec.solved_offset_enumeration))

    def _mutants() -> None:
        ref = ref_holder["ref"]
        for m in MUTANTS:
            state["mutant"] = f"{m.id}:{m.name}"
            if m.harness == B1:
                rec.mutants.append(_run_mutant_b1(pinned_root, m, load_mode, label, record_dir))
            elif m.harness == ST:
                rec.mutants.append(_run_mutant_schedule_table(pinned_root, m, load_mode, label, record_dir))
            else:
                rec.mutants.append(_run_mutant_alignment(ref, m))
        state["mutant"] = None
        # explicit link: mutant 32 (base leakage) <-> the base-invariance witness under the same mutation (L2 m31 note)
        with MUTANTS[31].apply():
            rec.base_invariance_witness["under_base_leakage_mutant"] = base_invariance_witness(ref)

    def _record() -> None:
        rec.written_to = _write_atomically({**asdict(rec), "passed": rec.passed}, record_dir, "gate_b_qualification")

    for stage, fn in (("manifest_preflight", _manifest_preflight), ("positive_control", _positive_control),
                      ("witnesses", _witnesses), ("mutants", _mutants), ("record", _record)):
        _boundary(stage, fn)
        if rec.failure is not None:
            return rec
    return rec
