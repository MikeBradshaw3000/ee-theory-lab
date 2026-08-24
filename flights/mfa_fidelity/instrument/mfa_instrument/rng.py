"""mfa_instrument.rng — Immutable seed provenance and role-specific stream discipline.

Spec anchors: Merge Specification v0.4 FROZEN §1.1 (single explicit Generator regime),
§6 (noise stream independent, non-interleaved; zero-amplitude => no construction).
Build Plan v0.2, L2 finding B: role-typed handles; child derivation from immutable
seed material, never by consuming draws; non-ancestor roles ABSENT (not idle) under
the Gate-A configuration.

CRITICAL Gate-A fact: the dynamics stream must be constructed EXACTLY as the ancestor
constructs it — np.random.default_rng(seed) — so the draw sequence is bit-identical
at matched seed (facts v1.1 S1(b): PRNG_SEED -> default_rng). It is therefore NOT
derived through the role registry. All other roles derive from SeedSequence
([root_seed, ROLE_CODE, *context]) and can never touch the dynamics sequence.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Optional, Tuple

import numpy as np

from .config import MICRO_UNITS, ConfigError, as_micro_units

# ---------------------------------------------------------------------------
# Frozen role codes (prospectively recorded; never renumbered).
# Dynamics deliberately has NO role code: it is not registry-derived.
# ---------------------------------------------------------------------------
ROLE_CODES: Dict[str, int] = {
    "noise": 1,                # eta_MFA stream (D4); constructed only if amplitude > 0
    "observable_null": 2,      # rebuilt B null machinery (spec S1(c)(5))
    "null_generation": 3,      # E1 reference template + replicate uniforms (E1 §4.2)
    "audit": 4,                # morphology generators, held-out ensembles (E1 §7)
    "bootstrap": 5,            # level-summary and envelope bootstrap (E1 §4.3, v0.6 §D)
    "projection_ensemble": 6,  # finite-N projection sweeps (T2-S/T2-L)
}


class RoleError(TypeError):
    """Raised when a stream is requested or injected outside its role discipline."""


@dataclass(frozen=True)
class RoleStream:
    """A typed handle: the role name travels with the Generator so a module cannot
    silently receive the wrong stream. Modules type-check `role` at their boundary."""
    role: str
    generator: np.random.Generator = field(repr=False)

    def expect(self, role: str) -> np.random.Generator:
        if self.role != role:
            raise RoleError(f"stream role {self.role!r} injected where {role!r} required")
        return self.generator


@dataclass(frozen=True)
class DynamicsStream:
    """The ancestor-faithful dynamics Generator. Deliberately a distinct type from
    RoleStream: no API accepts one where the other is required."""
    generator: np.random.Generator = field(repr=False)


class SeedRegistry:
    """Immutable root; derives role streams; records every derivation prospectively.

    - Dynamics: np.random.default_rng(root_seed), ancestor-identical construction.
    - Roles: np.random.default_rng(np.random.SeedSequence([root, code, *context])).
    - Derivation NEVER consumes draws from any existing stream.
    - gate_a_mode=True: only the dynamics stream may be constructed; every role
      request raises (absence, not idleness — the strongest bypass implementation).
    """

    def __init__(self, root_seed: int, gate_a_mode: bool = False) -> None:
        if not isinstance(root_seed, int) or root_seed < 0:
            raise ConfigError("root_seed must be a non-negative int")
        self._root = root_seed
        self._gate_a = bool(gate_a_mode)
        self._derivations: list[Tuple[str, Tuple[int, ...]]] = []
        self._dynamics_built = False

    # -- dynamics ----------------------------------------------------------
    def dynamics(self) -> DynamicsStream:
        if self._dynamics_built:
            raise RoleError("dynamics stream may be constructed exactly once per run")
        self._dynamics_built = True
        self._derivations.append(("dynamics", (self._root,)))
        return DynamicsStream(np.random.default_rng(self._root))

    # -- roles -------------------------------------------------------------
    def role(self, name: str, *context: int) -> RoleStream:
        if self._gate_a:
            raise RoleError(f"role stream {name!r} requested under Gate-A configuration: "
                            "non-ancestor stochastic roles must be ABSENT (spec §8.1)")
        if name not in ROLE_CODES:
            raise RoleError(f"unknown role {name!r}; legal roles: {sorted(ROLE_CODES)}")
        for c in context:
            if not isinstance(c, int) or c < 0:
                raise ConfigError("role context values must be non-negative ints")
        key = (self._root, ROLE_CODES[name], *context)
        self._derivations.append((name, key))
        seq = np.random.SeedSequence(list(key))
        return RoleStream(role=name, generator=np.random.default_rng(seq))

    def null_generation_for_level(self, m: float) -> RoleStream:
        """Level-keyed null stream: context = exact six-decimal micro-units of m
        (E1 v0.8 §C/E: integer micro-units are the canonical level identity)."""
        return self.role("null_generation", as_micro_units(m))

    def replicate_uniform_stream(self, replicate_index: int) -> RoleStream:
        """Replicate-keyed (NOT level-keyed) uniforms, reused identically across all m
        (E1 v0.6 §B: common random numbers across the dense grid)."""
        if replicate_index < 0:
            raise ConfigError("replicate_index must be >= 0")
        return self.role("null_generation", MICRO_UNITS + 1, replicate_index)

    # -- provenance --------------------------------------------------------
    def derivations(self) -> Tuple[Tuple[str, Tuple[int, ...]], ...]:
        """Every derivation performed, in order, for prospective recording in
        run_config/run_record. Read-only snapshot."""
        return tuple(self._derivations)


def make_noise_stream(registry: SeedRegistry, amplitude: float) -> Optional[RoleStream]:
    """D4 discipline: at amplitude 0, NO stream is constructed and None is returned —
    callers must branch on None, never on amplitude comparison against a live stream."""
    if amplitude == 0.0:
        return None
    return registry.role("noise")
