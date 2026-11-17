"""mfa_instrument/f9/streams.py — Flight 9 module M2 (stream half): the identity of one run and the
stream derived from it (Contract F9 v0.7 §2.5, §2.6, §2.10, §5.8, §8).

"Every run has its own derived stream, keyed by (panel master, terrain, composition, object,
initialization, κ in integer micro-units, seed index); nothing is paired between arms, objects or
levels."

THE KEY is that tuple, in that order, as seven non-negative integers. Terrain, composition, object and
initialization enter by the integer codes declared below (never renumbered). The run's tick stream is
    numpy.random.Generator(PCG64(SeedSequence(key))).
One run draws one further object from randomness outside its tick stream: the low-initialization
pattern of the T0 skeleton (§5.8, ρ₀ = 0.02). It comes from the INITIALIZATION-PATTERN stream,
SeedSequence(key + (INIT_PATTERN_ROLE,)), so that the pattern is independent of the run's tick draws
(the convention of the placed Flight 8 module, carried).

THIS MODULE HOLDS NO MASTER. The contract draws masters by stage (§8: calibration at step 4, canonical
at step 11, stability at step 14; "never all at once", DERIVED@BUILD), so a master is an argument,
supplied by the job that an authorization names. What is declared here about masters is only what a
master may not be:
  - not a master that an earlier instrument declared ("fresh masters throughout"): RETIRED_MASTERS lists every
    master declared in the placed E1 and Flight 8 source, and the Flight 9 probe's. The list excludes history
    only. That two stages of Flight 9 do not share a master is the runner's to enforce;
  - masters below TEST_MASTER_LIMIT are TEST masters. They exist so that the module's tests can run the
    rule without touching the space of real masters. `master_class` reports "test" or "stage"; a job of
    record must refuse a test master, and that refusal is the runner's.

SEEDS. A configuration has 40 runs, seed index 0..39 (§2.10). There is no seed panel: the index is the
last element of the key.

DECLARED COMBINATIONS (§2.6, §5.8). realization starts from the stationary floor-only state; skeleton
starts all-active; on T0 alone the skeleton also has the low start. Nothing else is a run.
"""
from __future__ import annotations

from typing import Dict, Tuple

import numpy as np

from . import config as C
from .config import F9ConfigError

# ----------------------------------------------------------------------------- codes (never renumbered)
TERRAIN_CODES: Tuple[Tuple[str, int], ...] = (
    ("T0", 0), ("TA", 1), ("TB", 2), ("TC", 3), ("TD-1-2", 4), ("TD-1-4", 5), ("TD-4-2", 6), ("TD-4-4", 7),
)
COMPOSITION_CODES: Tuple[Tuple[str, int], ...] = (("P", 0), ("H", 1))
OBJECT_CODES: Tuple[Tuple[str, int], ...] = (("realization", 0), ("skeleton", 1))
INIT_CODES: Tuple[Tuple[str, int], ...] = (("stationary_floor", 0), ("all_active", 1), ("low", 2))
INIT_PATTERN_ROLE = 1                             # appended to the key for the initialization-pattern stream

# object -> the initializations it may take; "low" on T0 only (§5.8)
OBJECT_INITS: Tuple[Tuple[str, Tuple[str, ...]], ...] = (("realization", ("stationary_floor",)), ("skeleton", ("all_active", "low")))
LOW_INIT_TERRAINS: Tuple[str, ...] = ("T0",)
RHO0_LOW_MICRO = 20_000                           # §5.8: skeleton-low ρ₀ = 0.02 (freeze record item 3), in micro-units

# ----------------------------------------------------------------------------- what a master may not be
RETIRED_MASTERS: Tuple[int, ...] = (
    # E1 (mfa_instrument/e1)
    20260917,                                         # config: seed panel
    202609171, 202609172,                             # null: template, validation replicates
    202609221, 202609222, 202609223,                  # audit: design, held-out, pricing (named retired in f8/audit.py)
    202609301, 202609302, 202609303, 202609304,       # projection: projection, tolerance, stability, bootstrap
    # Flight 8 (mfa_instrument/f8)
    20261026, 120261026,                              # config: canonical panel, calibration census
    220261026, 320261027,                             # null: validation attempts 1 and 2
    420261028,                                        # closure: projection
    520261028,                                        # evaluator: known-answer corpus
    620261102, 720261102, 820261102,                  # audit: design, held-out, pricing (prefixes 6, 7, 8 on the placement date)
    920261102,                                        # config: stability panel
    # Flight 9 noncanonical probe (contract §1.0: retired)
    9920261112,
)
TEST_MASTER_LIMIT = 1_000_000                     # 1 <= master < this: a test master
MASTER_LIMIT = 2 ** 64                            # a master is below this

STREAM_DECLARATION = (
    ("terrain_codes", TERRAIN_CODES), ("composition_codes", COMPOSITION_CODES), ("object_codes", OBJECT_CODES),
    ("init_codes", INIT_CODES), ("init_pattern_role", INIT_PATTERN_ROLE), ("object_inits", OBJECT_INITS),
    ("low_init_terrains", LOW_INIT_TERRAINS), ("rho0_low_micro", RHO0_LOW_MICRO), ("retired_masters", RETIRED_MASTERS),
    ("test_master_limit", TEST_MASTER_LIMIT), ("master_limit", MASTER_LIMIT),
    ("key_order", ("master", "terrain", "composition", "object", "initialization", "level_micro", "seed_index")),
    ("bit_generator", "PCG64"), ("seed_rule", "SeedSequence(list(key))"),
)
STREAM_DECLARATION_SHA256_LITERAL = "3274f728c79b6d44b3b2b0b685a4d7526ab0f4cd16f1d5e0e1bc72407e231832"


def verify_stream_declaration() -> str:
    """Recompute the stream declaration from the frozen configuration it must agree with; raise on any difference."""
    C.verify_frozen_identity()
    if tuple(n for n, _ in TERRAIN_CODES) != C.F9_TERRAINS or tuple(k for _, k in TERRAIN_CODES) != tuple(range(len(C.F9_TERRAINS))):
        raise F9ConfigError("terrain codes do not cover the declared terrains in order")
    if tuple(n for n, _ in COMPOSITION_CODES) != C.F9_COMPOSITIONS or tuple(k for _, k in COMPOSITION_CODES) != (0, 1):
        raise F9ConfigError("composition codes do not cover the declared compositions in order")
    for table in (OBJECT_CODES, INIT_CODES):
        if len({n for n, _ in table}) != len(table) or tuple(k for _, k in table) != tuple(range(len(table))):
            raise F9ConfigError("an object or initialization code table is not a bijection onto 0..n-1")
    if {o for o, _ in OBJECT_INITS} != {o for o, _ in OBJECT_CODES} or {i for _, ii in OBJECT_INITS for i in ii} != {i for i, _ in INIT_CODES}:
        raise F9ConfigError("the object/initialization table does not cover the declared objects and initializations")
    if RHO0_LOW_MICRO != 20_000 or not set(LOW_INIT_TERRAINS) <= set(C.F9_TERRAINS):
        raise F9ConfigError("the low initialization is not the one of contract §5.8")
    if len(RETIRED_MASTERS) != 21 or len(set(RETIRED_MASTERS)) != 21 or any(m < TEST_MASTER_LIMIT or m >= MASTER_LIMIT for m in RETIRED_MASTERS):
        raise F9ConfigError("the retired-master list is malformed")
    lit = STREAM_DECLARATION_SHA256_LITERAL
    if len(lit) != 64 or any(ch not in "0123456789abcdef" for ch in lit):
        raise F9ConfigError("stream declaration digest literal is not a 64-hex sha256 (no sentinel or placeholder is accepted)")
    if C.frozen_digest(STREAM_DECLARATION) != lit:
        raise F9ConfigError("stream declaration differs from its frozen literal digest")
    return lit


def _is_int(x) -> bool:
    return isinstance(x, int) and not isinstance(x, bool)


def check_master(master) -> int:
    """A master is an integer in [1, 2^64) that is not a retired master. Returns it."""
    if not _is_int(master) or not (1 <= master < MASTER_LIMIT): raise F9ConfigError(f"not a master: {master!r}")
    if master in RETIRED_MASTERS: raise F9ConfigError(f"master {master} is retired and may not be used again")
    return master


def master_class(master) -> str:
    """'test' below TEST_MASTER_LIMIT, otherwise 'stage'. A job of record refuses a test master (the runner's check)."""
    return "test" if check_master(master) < TEST_MASTER_LIMIT else "stage"


def check_run_identity(master, terrain, composition, obj, init, level_micro, seed_index) -> None:
    """Refuse anything that is not a declared run (see DECLARED COMBINATIONS)."""
    check_master(master)
    if (terrain, composition) not in C.F9_ARMS: raise F9ConfigError(f"not a declared arm: {terrain!r}.{composition!r}")
    if obj not in dict(OBJECT_INITS): raise F9ConfigError(f"not a declared object: {obj!r}")
    if init not in dict(OBJECT_INITS)[obj]: raise F9ConfigError(f"object {obj!r} does not take initialization {init!r}")
    if init == "low" and terrain not in LOW_INIT_TERRAINS: raise F9ConfigError("the low initialization is declared on T0 only (contract §5.8)")
    C.level_id(level_micro)                           # refuses an undeclared level, a bool or a non-integer
    if not _is_int(seed_index) or not (0 <= seed_index < C.F9_N_SEEDS): raise F9ConfigError(f"not a seed index: {seed_index!r}")


def stream_key(master, terrain, composition, obj, init, level_micro, seed_index) -> Tuple[int, ...]:
    """(panel master, terrain, composition, object, initialization, κ in micro-units, seed index) as seven integers (§2.5)."""
    check_run_identity(master, terrain, composition, obj, init, level_micro, seed_index)
    return (master, dict(TERRAIN_CODES)[terrain], dict(COMPOSITION_CODES)[composition], dict(OBJECT_CODES)[obj],
            dict(INIT_CODES)[init], level_micro, seed_index)


def _check_key(key) -> Tuple[int, ...]:
    if not isinstance(key, tuple) or len(key) != 7 or not all(_is_int(k) and k >= 0 for k in key): raise F9ConfigError("a stream key is seven non-negative integers")
    inv = lambda table: {k: n for n, k in table}
    try:
        names = (inv(TERRAIN_CODES)[key[1]], inv(COMPOSITION_CODES)[key[2]], inv(OBJECT_CODES)[key[3]], inv(INIT_CODES)[key[4]])
    except KeyError:
        raise F9ConfigError("a stream key carries an undeclared code")
    check_run_identity(key[0], names[0], names[1], names[2], names[3], key[5], key[6])
    return key


def generator_from_key(key) -> np.random.Generator:
    """The run's tick stream. The executed stream IS the recorded key."""
    return np.random.Generator(np.random.PCG64(np.random.SeedSequence(list(_check_key(key)))))


def init_pattern_generator(key) -> np.random.Generator:
    """The initialization-pattern stream of the same run: the key with INIT_PATTERN_ROLE appended."""
    return np.random.Generator(np.random.PCG64(np.random.SeedSequence(list(_check_key(key)) + [INIT_PATTERN_ROLE])))


def code_tables() -> Dict[str, Dict[str, int]]:
    return {"terrain": dict(TERRAIN_CODES), "composition": dict(COMPOSITION_CODES), "object": dict(OBJECT_CODES), "initialization": dict(INIT_CODES)}
