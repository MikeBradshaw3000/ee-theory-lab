"""tests/test_f9_m1.py — Flight 9 module M1: the frozen declarations verify against their rules and against the frozen
contract and freeze record; terrains have the properties Contract F9 v0.7 §3 states; the edge tracer gives the
components §5.5 step 3 defines (fixed cases, L2's two-loop case, and an independent tracer on random masks); the
registered family is every level set of the comparison array; the spectral routine agrees with a dense eigenvalue
computation; the identity bundle round-trips and refuses tampering; nothing in e1 or f8 is touched. The tests marked
"L2 M1 round 1" are the closure tests of that review's R1, R2 and R3.

Platform policy. Values that pass through cos or tanh are compared with tolerances, never by hash. The registered
family SIZES of the frozen contract are container values and provisional (§3.4 step 1): `test_container_values_are_reported`
reports agreement and asserts nothing about them, because a value within an ulp of a rounding boundary may round the
other way on another libm. Exact assertions are made only where no libm is involved (T0, the TD cores, declared literals)."""
import hashlib
import json
import math
import os
import shutil
import struct

import numpy as np
import pytest

from mfa_instrument.f9 import config as C
from mfa_instrument.f9 import family as F
from mfa_instrument.f9 import geometry as G
from mfa_instrument.f9 import identities as I
from mfa_instrument.f9 import spectral as S
from mfa_instrument.f9 import terrain as T

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, "..", "..", "..", ".."))
CONTRACT = os.path.join(REPO, "flights", "mfa_fidelity", "contracts", "flight9", "FLIGHT_9_CONTRACT_v0_7.md")
FREEZE_RECORD = os.path.join(REPO, "flights", "mfa_fidelity", "contracts", "flight9", "FLIGHT_9_FREEZE_RECORD.md")
PKG = os.path.join(HERE, "..", "mfa_instrument")
L = C.F9_GRID


def _sha_lf(path):
    """SHA-256 of a committed text file as its LF blob: a Windows working copy may hold CRLF (core.autocrlf)."""
    with open(path, "rb") as fh: return hashlib.sha256(fh.read().replace(b"\r\n", b"\n")).hexdigest()


# ======================= frozen declarations =======================
def test_frozen_identity_and_the_committed_contract():
    out = C.verify_frozen_identity()
    assert out["version"] == "f9_stage1_v1"
    assert _sha_lf(CONTRACT) == C.F9_CONTRACT_SHA256
    assert _sha_lf(FREEZE_RECORD) == C.F9_FREEZE_RECORD_SHA256


def test_levels_follow_the_rule_of_section_2_9():
    lv = C.F9_LEVELS_MICRO
    assert lv == C.generate_levels_micro() and len(lv) == 25
    assert lv[0] == 750000 and lv[-3:] == (2250000, 2500000, 3000000)
    assert lv[1:22] == tuple(1000000 + 50000 * k for k in range(21))
    assert C.level_id(1050000) == "1.050000" and C.level_id(750000) == "0.750000"
    with pytest.raises(C.F9ConfigError): C.level_id(1025000)
    with pytest.raises(C.F9ConfigError): C.level_id(True)


def test_declared_values_are_the_freeze_records():
    assert (C.F9_GRID, C.F9_TICKS, C.F9_TAIL_TICKS, C.F9_N_SEEDS, C.F9_SURVIVAL_MIN) == (100, 3000, 1000, 40, 36)
    assert C.F9_THETA_MICRO == 200000 and C.F9_THETA_REPORTED_MICRO == (100000, 300000)
    assert (C.F9_INFORMATIVE_MIN_CELLS, C.F9_INFORMATIVE_MIN_BONDS, C.F9_COMPONENT_MIN_BONDS, C.F9_EPSILON_MICRO) == (100, 40, 40, 2000000)
    assert C.F9_ROUND_PLACES == 12 and C.F9_MU == 0.2 and C.F9_ETA0 == -math.log(0.99)
    assert abs(C.q_deact() - 0.181269) < 5e-7                                  # contract §2.7, A.3
    assert len(C.F9_ARMS) == 15 and C.F9_ARMS[0] == ("T0", "P") and ("T0", "H") not in C.F9_ARMS
    assert sum(1 for t, c in C.F9_ARMS if c == "P" and t != "T0") == 7 == sum(1 for t, c in C.F9_ARMS if c == "H")


def test_a_changed_literal_fails_the_preflight(monkeypatch):
    monkeypatch.setattr(C, "F9_DECLARATION", C.F9_DECLARATION + (("extra", 1),))
    with pytest.raises(C.F9ConfigError): C.verify_frozen_identity()
    monkeypatch.undo()
    monkeypatch.setattr(C, "F9_DECLARATION_SHA256_LITERAL", "0" * 63 + "g")
    with pytest.raises(C.F9ConfigError): C.verify_frozen_identity()


def test_floor_hazard_is_bound_to_its_rule_l2_m1_round1_r3(monkeypatch):
    """L2 M1 round 1, R3: the float η₀ is outside the declaration digest, so the preflight must check it against the
    digested rule and probability. A changed η₀ fails; the digest does not depend on the float."""
    assert C.F9_ETA0 == -math.log(1.0 - C.F9_FLOOR_PROBABILITY) and C.F9_FLOOR_PROBABILITY == 0.01
    assert ("floor_probability", 0.01) in C.F9_DECLARATION and ("eta0_rule", "-ln(1 - floor_probability)") in C.F9_DECLARATION
    assert not any(k == "eta0" for k, _v in C.F9_DECLARATION)
    before = C.frozen_digest(C.F9_DECLARATION)
    monkeypatch.setattr(C, "F9_ETA0", -math.log(1.0 - 0.02))
    assert C.frozen_digest(C.F9_DECLARATION) == before                        # the digest is unchanged ...
    with pytest.raises(C.F9ConfigError): C.verify_frozen_identity()           # ... and the preflight refuses
    with pytest.raises(C.F9ConfigError): I.build_identity_record()            # so does the identity build
    monkeypatch.setattr(C, "F9_ETA0", float(np.nextafter(-math.log(0.99), 1.0)))   # one ulp off is also not the rule's value here
    with pytest.raises(C.F9ConfigError): C.verify_frozen_identity()
    monkeypatch.undo()
    monkeypatch.setattr(C, "F9_FLOOR_PROBABILITY", 0.02)                      # the probability literal is inside the digest
    with pytest.raises(C.F9ConfigError): C.verify_frozen_identity()
    monkeypatch.undo()
    assert C.verify_frozen_identity()["declaration_sha256"] == C.F9_DECLARATION_SHA256_LITERAL


# ======================= terrains =======================
# contract Appendix A.1: base range, λ^P range, λ^H range (4 decimals)
A1 = {"T0": (0.8, 0.8, 0.512, 0.512, 0.8, 0.8), "TA": (0.300, 0.900, 0.0270, 0.7290, 0.3000, 0.9000),
      "TB": (0.100, 1.000, 0.0258, 0.1153, 0.4200, 0.5133), "TC": (0.050, 0.900, 0.0405, 0.7290, 0.6167, 0.9000),
      "TD-1-2": (0.300, 0.900, 0.0270, 0.7290, 0.3000, 0.9000), "TD-1-4": (0.300, 0.900, 0.0270, 0.7290, 0.3000, 0.9000),
      "TD-4-2": (0.300, 0.900, 0.0270, 0.7290, 0.3000, 0.9000), "TD-4-4": (0.300, 0.898, 0.0270, 0.7253, 0.3000, 0.8985)}


@pytest.mark.parametrize("name", C.F9_TERRAINS)
def test_bases_have_the_declared_form_and_ranges(name):
    v, u, r = T.bases(name)
    for b in (v, u, r):
        assert b.dtype == np.float64 and b.shape == (L, L) and b.flags["C_CONTIGUOUS"] and 0.0 <= b.min() and b.max() <= 1.0
    lo, hi, plo, phi, hlo, hhi = A1[name]
    assert abs(min(v.min(), u.min(), r.min()) - lo) < 6e-4 and abs(max(v.max(), u.max(), r.max()) - hi) < 6e-4
    P = T.compose("P", v, u, r); H = T.compose("H", v, u, r)
    assert abs(P.min() - plo) < 6e-5 and abs(P.max() - phi) < 6e-5 and abs(H.min() - hlo) < 6e-5 and abs(H.max() - hhi) < 6e-5
    assert np.array_equal(P, v * u * r) and np.array_equal(H, (v + u + r) / 3.0)


def test_t0_is_flat_and_its_identity_is_exact():
    v, u, r = T.bases("T0")
    assert np.all(v == 0.8) and np.all(u == 0.8) and np.all(r == 0.8)
    assert T.base_identity("T0").startswith("21babaa5c51d9630")            # contract A.1; no libm enters T0
    assert T.base_identity("T0") == hashlib.sha256(np.full((3, L, L), 0.8, dtype="<f8").tobytes()).hexdigest()


def test_axis_zero_is_x_and_formulas_match_cell_by_cell():
    c = lambda z: math.cos(2.0 * math.pi * z)
    v, u, r = T.bases("TA")
    for i, j in ((0, 0), (25, 0), (0, 50), (37, 81)):
        assert abs(v[i, j] - (0.6 + 0.15 * (c(i / L) + c(j / L)))) < 1e-14 and v[i, j] == u[i, j] == r[i, j]
    v, u, r = T.bases("TB")
    for i, j in ((0, 0), (25, 0), (0, 50), (37, 81)):
        s = 0.55 + 0.07 * c(i / L); d = 0.19 + 0.19 * c(j / L)
        assert abs(v[i, j] - (s + d)) < 1e-14 and abs(u[i, j] - (s - d)) < 1e-14 and r[i, j] == 0.3
    H = T.compose("H", v, u, r)
    assert float(np.max(np.abs(H - H[:, :1]))) < 1e-15                      # the height index varies along x only (§3.2)
    v, u, r = T.bases("TC")
    assert np.all(v == 0.9) and np.all(r == 0.9) and abs(u[50, 50] - 0.05) < 1e-14 and abs(u[0, 0] - 0.9) < 1e-14


def test_tb_criterion_and_roles():
    sh = T.tb_variance_shares()
    assert abs(sh["x"] - 0.5173) < 5e-5 and abs(sh["y"] - 0.4827) < 5e-5 and abs(sh["additive_residual"]) < 1e-15
    assert C.F9_TB_X_SHARE_RANGE[0] <= sh["x"] <= C.F9_TB_X_SHARE_RANGE[1]
    H = T.raw_index("TB", "H"); assert abs(H.max() / H.min() - 1.22) < 5e-3
    cf = T.tb_cross_fall(); assert abs(cf["H_along_P"] - 0.0876) < 5e-5      # §3.3: TB's two families differ
    for name, _lat in C.F9_SAME_FAMILY_LATENT:                              # §3.3: elsewhere the raw index never falls along ω
        for comp in C.F9_COMPOSITIONS: assert T.monotone_violation(name, comp) <= 1e-12


# contract §3.2 table: lattice perimeter of C, band cells (10–90% of the base step), largest base step per cell
TD_TABLE = {"TD-1-2": (200, 676, 0.145), "TD-1-4": (200, 1376, 0.074), "TD-4-2": (416, 1424, 0.142), "TD-4-4": (416, 2816, 0.074)}


@pytest.mark.parametrize("name", sorted(TD_TABLE))
def test_td_core_and_margin_table(name):
    perim, band, step = TD_TABLE[name]
    core = T.td_core(name); e = G.edge(core)
    assert int(core.sum()) == 2000 and e.n_bonds == perim
    assert float(np.abs(T.td_delta(name)).min()) >= 0.03
    assert e.component_sizes() == ((200,) if name.startswith("TD-1") else (104, 104, 104, 104))
    t = T.bases(name)[0]
    assert int(((t > 0.3 + 0.06) & (t < 0.9 - 0.06)).sum()) == band        # 10% and 90% of the 0.6 step
    steps = max(float(np.abs(t - np.roll(t, 1, a)).max()) for a in (0, 1))
    assert abs(steps - step) < 5e-4
    assert np.array_equal(core, T.td_delta(name) > 0)


def test_td_cores_are_fixed_sets_independent_of_w():
    assert np.array_equal(T.td_core("TD-1-2"), T.td_core("TD-1-4")) and np.array_equal(T.td_core("TD-4-2"), T.td_core("TD-4-4"))
    assert not np.array_equal(T.td_core("TD-1-2"), T.td_core("TD-4-2"))


def test_undeclared_objects_are_refused():
    for bad in ("TE", "t0", "", None):
        with pytest.raises(C.F9ConfigError): T.bases(bad)
    v, u, r = T.bases("T0")
    with pytest.raises(C.F9ConfigError): T.compose("X", v, u, r)
    with pytest.raises(C.F9ConfigError): T.comparison_array("TA", "X")
    with pytest.raises(C.F9ConfigError): C.td_params("TA")


def test_serialization_is_little_endian_c_order_and_round_trips():
    v, u, r = T.bases("TB")
    raw = T.serialize(v)
    assert len(raw) == 8 * L * L and raw == v.astype("<f8").tobytes(order="C")
    assert np.array_equal(T.deserialize(raw), v)
    assert np.frombuffer(raw[:8 * L], dtype="<f8")[1] == v[0, 1] != v[1, 0]   # row-major: the second value is (0, 1)
    assert T.base_identity("TB") == hashlib.sha256(T.serialize(v) + T.serialize(u) + T.serialize(r)).hexdigest()
    with pytest.raises(C.F9ConfigError): T.serialize(v[:50])
    with pytest.raises(C.F9ConfigError): T.deserialize(raw[:-8])


# ======================= comparison arrays =======================
def test_comparison_arrays_follow_section_3_4_step_3():
    for name, latent in C.F9_SAME_FAMILY_LATENT:
        oP, oH = T.comparison_array(name, "P"), T.comparison_array(name, "H")
        v, u, r = T.bases(name)
        assert np.array_equal(oP, oH) and np.array_equal(oP, np.round({"v": v, "u": u}[latent], 12))
    oP, oH = T.comparison_array("TB", "P"), T.comparison_array("TB", "H")
    assert not np.array_equal(oP, oH)
    assert np.array_equal(oP, np.round(T.raw_index("TB", "P"), 12)) and np.array_equal(oH, np.round(T.raw_index("TB", "H"), 12))
    for name, comp in C.F9_ARMS:                                            # rounded: every value is a 12-place decimal
        om = T.comparison_array(name, comp)
        assert om.dtype == np.float64 and np.array_equal(om, np.round(om, 12))
        assert float(np.max(np.abs(om - np.round(om * 1e12) / 1e12))) < 1e-15


def test_level_labels_are_the_compositions_own_index():
    assert T.level_label("TA", "P", 0.5) == 0.125 and T.level_label("TA", "H", 0.5) == 0.5
    assert T.level_label("TD-4-2", "P", 0.3) == 0.3 ** 3
    assert abs(T.level_label("TC", "P", 0.5) - 0.405) < 1e-15 and abs(T.level_label("TC", "H", 0.6) - 0.8) < 1e-15
    assert T.level_label("TB", "P", 0.07) == 0.07
    with pytest.raises(C.F9ConfigError): T.level_label("T0", "P", 0.8)
    with pytest.raises(C.F9ConfigError): T.level_label("TA", "X", 0.5)
    with pytest.raises(C.F9ConfigError): T.level_label("TD-9-9", "P", 0.5)


# ======================= edge and components (§5.5 step 3) =======================
def _mask(cells):
    m = np.zeros((L, L), dtype=bool)
    for i, j in cells: m[i % L, j % L] = True
    return m


def _trace_cycles(mask):
    """An independent tracer: walk each boundary loop with the region on the left. At the end of the east side of cell c
    travelling north: if the north neighbour is outside, turn left onto c's north side; else if the north-east cell is
    outside, go straight onto the north neighbour's east side; else turn right onto the north-east cell's south side.
    A diagonal contact therefore turns left around its own cell (4-connected region). Returns the sorted loop lengths."""
    D = ((0, 1), (-1, 0), (0, -1), (1, 0))             # outward normal of side k of a cell: +j (east), -i (north), -j (west), +i (south)
    m = mask
    start = {(i, j, k) for i in range(L) for j in range(L) if m[i, j] for k in range(4) if not m[(i + D[k][0]) % L, (j + D[k][1]) % L]}
    seen = set(); loops = []
    for s in sorted(start):
        if s in seen: continue
        n = 0; cur = s
        while cur not in seen:
            seen.add(cur); n += 1
            i, j, k = cur
            ahead = D[(k + 1) % 4]                    # the direction of travel (counter-clockwise around the cell)
            out = D[k]
            a = ((i + ahead[0]) % L, (j + ahead[1]) % L)                          # the cell ahead on the region side
            b = ((i + ahead[0] + out[0]) % L, (j + ahead[1] + out[1]) % L)        # the cell ahead on the outer side
            if not m[a]: cur = (i, j, (k + 1) % 4)
            elif not m[b]: cur = (a[0], a[1], k)
            else: cur = (b[0], b[1], (k - 1) % 4)
        loops.append(n)
    assert seen == start
    return sorted(loops)


def test_fixed_cases_of_the_component_convention():
    e = G.edge(_mask([(10, 10)])); assert e.n_bonds == 4 and e.component_sizes() == (4,)
    e = G.edge(_mask([(10, 10), (11, 11)])); assert e.n_bonds == 8 and sorted(e.component_sizes()) == [4, 4]      # corner contact: separate
    e = G.edge(_mask([(10, 10), (10, 11)])); assert e.n_bonds == 6 and e.component_sizes() == (6,)                # side contact: one
    ring = _mask([(i, j) for i in range(10, 13) for j in range(10, 13) if (i, j) != (11, 11)])
    assert sorted(G.edge(ring).component_sizes()) == [4, 12]                                                      # a hole has its own component
    strip = np.zeros((L, L), dtype=bool); strip[20:25, :] = True
    assert G.edge(strip).component_sizes() == (L, L)                                                             # a wrapping strip has two
    block = np.zeros((L, L), dtype=bool); block[95:, 95:] = True; block[:3, :3] = True                            # two blocks meeting at the periodic corner
    assert sorted(G.edge(block).component_sizes()) == [12, 20]
    wrap = np.zeros((L, L), dtype=bool); wrap[98:, 40:60] = True; wrap[:2, 40:60] = True                          # one block across the seam
    assert G.edge(wrap).component_sizes() == (48,)
    assert G.edge(np.zeros((L, L), dtype=bool)).n_bonds == 0 and G.edge(np.ones((L, L), dtype=bool)).n_components == 0
    hole_in_complement = ~_mask([(10, 10), (11, 11)])                                                             # the complement is 8-connected: one loop of 8
    assert G.edge(hole_in_complement).component_sizes() == (8,)


def test_l2_two_loop_case_has_two_components():
    """L2 round 2, F1: a wrapping strip whose left side zigzags. Its two sides are separate boundaries."""
    x, y = np.indices((L, L)); a = np.where(y % 2 == 0, 2, 40)
    for hi in (60, 70):
        e = G.edge((x >= a) & (x < hi))
        assert e.n_bonds == 4000 and sorted(e.component_sizes()) == [100, 3900]
        straight = e.component[np.isclose(e.points[:, 0], hi - 0.5)]
        assert len(straight) == 100 and len(set(straight.tolist())) == 1


def test_canonical_bond_order_and_midpoints():
    e = G.edge(_mask([(10, 10)]))
    assert e.points.tolist() == [[9.5, 10.0], [10.5, 10.0], [10.0, 9.5], [10.0, 10.5]] and e.component.tolist() == [0, 0, 0, 0]
    e = G.edge(_mask([(0, 0)]))                                             # wrapping midpoints stay in [0, L)
    assert e.points.tolist() == [[0.5, 0.0], [L - 0.5, 0.0], [0.0, 0.5], [0.0, L - 0.5]]
    e = G.edge(_mask([(10, 10), (50, 50)])); assert e.component.tolist() == [0, 0, 1, 1, 0, 0, 1, 1]            # first appearance
    with pytest.raises(C.F9ConfigError): G.edge(np.zeros((L, L), dtype=np.int64))
    with pytest.raises(C.F9ConfigError): G.edge(np.zeros((L, L - 1), dtype=bool))


def test_tracer_agrees_with_an_independent_walk_on_random_masks():
    rng = np.random.default_rng(20261116)                                    # a test stream; binds nothing
    for trial in range(60):
        p = (0.08, 0.3, 0.5, 0.7, 0.92)[trial % 5]
        m = rng.random((L, L)) < p
        if trial % 3 == 0:                                                   # smoother regions as well as salt and pepper
            f = sum(np.roll(np.roll(m.astype(float), a, 0), b, 1) for a in (-1, 0, 1) for b in (-1, 0, 1)) / 9.0
            m = f >= 0.5
        e = G.edge(m)
        assert sorted(e.component_sizes()) == _trace_cycles(m)
        assert e.n_bonds == int((m != np.roll(m, 1, 0)).sum() + (m != np.roll(m, 1, 1)).sum())
        if e.n_bonds:
            comp = e.component; first = [int(np.flatnonzero(comp == k)[0]) for k in range(e.n_components)]
            assert first == sorted(first)                                    # numbered by first appearance


def test_a_region_and_its_complement_share_bonds_not_components():
    m = _mask([(10, 10), (11, 11)])
    a, b = G.edge(m), G.edge(~m)
    assert np.array_equal(a.points, b.points) and a.n_components == 2 and b.n_components == 1


def test_informative_level_thresholds():
    blk = np.zeros((L, L), dtype=bool); blk[:10, :10] = True                # 100 cells, 40 bonds: the least informative square
    assert G.is_informative(blk)
    small = np.zeros((L, L), dtype=bool); small[:9, :11] = True             # 99 cells
    assert not G.is_informative(small) and not G.is_informative(~small)
    thin = np.zeros((L, L), dtype=bool); thin[:10, :9] = True; thin[10, :9] = True; thin[11, 0] = True          # 100 cells
    assert int(thin.sum()) == 100 and G.is_informative(thin)
    assert not G.is_informative(np.zeros((L, L), dtype=bool)) and not G.is_informative(np.ones((L, L), dtype=bool))


# ======================= the registered family (§5.5 step 5) =======================
@pytest.mark.parametrize("name,comp", [(t, c) for t, c in C.F9_ARMS if t != "T0"])
def test_family_is_every_level_set_of_the_comparison_array(name, comp):
    om = T.comparison_array(name, comp); fam = F.Family(om)
    vals = np.unique(om)
    assert fam.levels == tuple(float(x) for x in vals[1:]) and len(fam) == len(vals) - 1 >= 1
    prev = None
    for ell in fam.levels[:: max(1, len(fam) // 40)] + (fam.levels[0], fam.levels[-1]):
        m = fam.mask(ell); k = int(m.sum())
        assert 0 < k < L * L and np.array_equal(m, om >= ell) and k == int((om >= ell).sum())
    counts = [int((om >= ell).sum()) for ell in fam.levels]
    assert counts == sorted(counts, reverse=True) and len(set(counts)) == len(counts)       # strictly nested: no two equal
    with pytest.raises(C.F9ConfigError): fam.mask(float(vals[0]))                           # the minimum is not a level
    with pytest.raises(C.F9ConfigError): fam.mask(float(vals[1]) + 1e-13)


def test_constant_index_has_an_empty_family():
    for comp in ("P",):
        fam = F.Family(T.comparison_array("T0", comp))
        assert fam.is_empty and len(fam) == 0
    s = F.family_summary(T.comparison_array("T0", "P"))
    assert s["n_levels"] == 0 and s["bonds_max"] is None


def test_same_family_terrains_share_masks_and_tb_does_not():
    for name, _lat in C.F9_SAME_FAMILY_LATENT:
        assert F.masks_identity(T.comparison_array(name, "P")) == F.masks_identity(T.comparison_array(name, "H"))
    assert F.masks_identity(T.comparison_array("TB", "P")) != F.masks_identity(T.comparison_array("TB", "H"))


def test_family_identities_distinguish_levels_masks_and_components():
    om = T.comparison_array("TD-4-2", "P"); a = F.family_summary(om)
    assert a["masks_sha256"] == F.masks_identity(om) and a == F.family_summary(om.copy())
    b = F.family_summary(np.round(om * 0.5, 12))                              # same nested masks, different level values
    assert b["masks_sha256"] == a["masks_sha256"] and b["family_sha256"] != a["family_sha256"] and b["components_sha256"] == a["components_sha256"]
    c = F.family_summary(np.roll(om, 1, axis=0))                             # translated: different masks, same shapes
    assert c["masks_sha256"] != a["masks_sha256"] and c["n_levels"] == a["n_levels"] and c["bonds_max"] == a["bonds_max"]
    assert a["components_max"] == 4 and a["bonds_max"] == 768                # the longest canonical contour (contract §6.2)
    tbh = F.family_summary(T.comparison_array("TB", "H"))
    assert tbh["bonds_min"] == tbh["bonds_max"] == 200 and tbh["components_max"] == 2      # lines of constant x: two sides


def test_component_identity_binds_membership_l2_m1_round1_r1(monkeypatch):
    """L2 M1 round 1, R1: on a 10-cell checkerboard the region's tracing and the complement's corner pairing give the same
    bonds, the same 50 components of 40 bonds each, and different membership. The component identity must tell them
    apart while the masks stay the same; and the tracer of record must be the region's."""
    x, y = np.indices((L, L)); omega = ((x // 10 + y // 10) % 2).astype(np.float64); mask = omega >= 1
    correct, other = G.edge(mask), G.edge(~mask)
    assert np.array_equal(correct.points, other.points) and correct.component_sizes() == other.component_sizes() == (40,) * 50
    assert int(np.count_nonzero(correct.component != other.component)) == 1500
    a = F.family_summary(omega)
    original = G.edge
    monkeypatch.setattr(G, "edge", lambda m: original(~m))
    b = F.family_summary(omega)
    monkeypatch.undo()
    assert a["masks_sha256"] == b["masks_sha256"] and a["family_sha256"] == b["family_sha256"] and a["bonds_max"] == b["bonds_max"]
    assert a["components_sha256"] != b["components_sha256"]
    # the identity is the declared serialization of the region's own partition
    h = hashlib.sha256(); h.update(struct.pack("<ii", 2000, 50)); h.update(np.asarray(correct.component, dtype="<i4").tobytes())
    assert a["components_sha256"] == h.hexdigest()
    # and the region's partition is the right one: each 10×10 block of the region is one component (4-connected region)
    for k in range(correct.n_components):
        pts = correct.points[correct.component == k]
        cells = {(int(np.floor(px + 0.5)) % L // 10, int(np.floor(py + 0.5)) % L // 10) for px, py in pts}
        inside = [c for c in cells if (c[0] + c[1]) % 2 == 1]
        assert len(pts) == 40 and len(inside) == 1


def test_family_level_bytes_are_little_endian_l2_m1_round1_r1():
    """L2 M1 round 1, R1 (contained): the level enters the family identity as struct '<d', whatever the host byte order."""
    omega = np.zeros((L, L)); omega[:50] = 1.25
    h = hashlib.sha256(); h.update(struct.pack("<d", 1.25)); h.update(np.packbits((omega >= 1.25).ravel()).tobytes())
    assert F.family_summary(omega)["family_sha256"] == h.hexdigest()
    assert struct.pack("<d", 1.25).hex() == "000000000000f43f" and struct.pack(">d", 1.25).hex() == "3ff4000000000000"


def test_family_refuses_malformed_arrays():
    with pytest.raises(C.F9ConfigError): F.Family(np.zeros((L, L), dtype=np.float32))
    bad = np.zeros((L, L)); bad[0, 0] = np.nan
    with pytest.raises(C.F9ConfigError): F.Family(bad)


# ======================= spectral-relative gain (§2.8) =======================
A1_SPR = {"T0": (0.512000, 0.800000), "TA": (0.701413, 0.880236), "TB": (0.113406, 0.509168), "TC": (0.728367, 0.899373),
          "TD-1-2": (0.725886, 0.896516), "TD-1-4": (0.723752, 0.894862), "TD-4-2": (0.713340, 0.884323), "TD-4-4": (0.690069, 0.869999)}
A1_GSPEC = {"T0": (0.354041, 0.226587), "TA": (0.258435, 0.205933), "TB": (1.598403, 0.356011), "TC": (0.248871, 0.201551),
            "TD-1-2": (0.249721, 0.202193), "TD-1-4": (0.250458, 0.202567), "TD-4-2": (0.254113, 0.204981), "TD-4-4": (0.262683, 0.208356)}


@pytest.mark.parametrize("name", C.F9_TERRAINS)
def test_spectral_values_agree_with_appendix_a(name):
    for k, comp in enumerate(C.F9_COMPOSITIONS):
        lam = T.raw_index(name, comp); spr = S.spectral_radius(lam)
        assert abs(spr - A1_SPR[name][k]) < 1e-6 and abs(S.g_spec(lam) - A1_GSPEC[name][k]) < 2e-6
        assert lam.mean() <= spr + 1e-12 and spr <= lam.max() + 1e-12        # A/8 is doubly stochastic: mean(λ) ≤ spr ≤ max(λ)


def test_power_iteration_agrees_with_a_dense_eigenvalue_computation():
    rng = np.random.default_rng(20261116)
    for n in (6, 9, 12):
        lam = rng.random((n, n)) * 0.9 + 0.05
        N = n * n; A = np.zeros((N, N))
        for i in range(n):
            for j in range(n):
                for di in (-1, 0, 1):
                    for dj in (-1, 0, 1):
                        if di or dj: A[i * n + j, ((i + di) % n) * n + (j + dj) % n] += 1.0
        dense = float(np.max(np.abs(np.linalg.eigvals(np.diag(lam.ravel()) @ A / 8.0))))
        assert abs(S.spectral_radius(lam) - dense) < 1e-9 * dense


def test_routine_agrees_with_lanczos_on_every_arm():
    """The committed routine stops on the change of the Rayleigh quotient, which does not bound its error. This checks
    the error directly against an independent method, to the contract's 1e-9 relative (§2.8). Skipped without scipy."""
    sla = pytest.importorskip("scipy.sparse.linalg")
    from mfa_instrument.dynamics import _moore_sum_a
    for name, comp in C.F9_ARMS:
        lam = T.raw_index(name, comp); s = np.sqrt(lam)
        op = sla.LinearOperator((lam.size, lam.size), matvec=lambda w: (s * _moore_sum_a(s * w.reshape(lam.shape)) / 8.0).ravel(), dtype=np.float64)
        ref = float(sla.eigsh(op, k=1, which="LA", tol=1e-14, ncv=40, maxiter=20000)[0][0])
        spr = S.spectral_radius(lam)
        assert spr <= ref * (1.0 + 1e-13) and (ref - spr) <= C.F9_SPR_RECOMPUTE_RTOL * ref


def test_flat_terrain_reduces_to_flight_8s_control():
    lam = T.raw_index("T0", "P"); gs = S.g_spec(lam)
    assert abs(S.spectral_radius(lam) - 0.512) < 1e-13 and abs(gs - C.q_deact() / 0.512) < 1e-13
    m = S.local_m(lam, S.gain(1000000, gs))                                # κ = 1 on a flat terrain is m = 1 everywhere (notation v1.2 §2b)
    assert float(np.max(np.abs(m - 1.0))) < 1e-12
    assert abs(S.gain(1500000, gs) - 1.5 * gs) < 1e-15
    with pytest.raises(C.F9ConfigError): S.gain(1234567, gs)


def test_every_declared_arm_is_in_the_routines_domain():
    """The routine is of record for strictly positive indices (spectral.py, DOMAIN). Every declared arm is one; and the
    documented example outside the domain behaves as documented, so the limitation is known and not relied on."""
    for name, comp in C.F9_ARMS: assert float(T.raw_index(name, comp).min()) > 0.0
    k13 = np.zeros((8, 8)); k13[3, 3] = k13[2, 2] = k13[2, 4] = k13[4, 3] = 1.0
    assert abs(S.spectral_radius(k13) - 0.1875) < 1e-6 and abs(math.sqrt(3) / 8 - 0.21650635094610965) < 1e-15


def test_zero_index_has_no_level():
    z = np.zeros((L, L))
    assert S.spectral_radius(z) == 0.0
    with pytest.raises(C.F9ConfigError): S.g_spec(z)
    with pytest.raises(C.F9ConfigError): S.spectral_radius(-np.ones((4, 4)))
    with pytest.raises(C.F9ConfigError): S.spectral_radius(np.ones((4, 5)))


# ======================= the identity build (§3.4 step 4) =======================
@pytest.fixture(scope="module")
def bundle(tmp_path_factory):
    d = str(tmp_path_factory.mktemp("f9_identities"))
    return d, I.write_bundle(d)


def test_record_covers_every_declared_object(bundle):
    d, rec = bundle
    assert rec["type"] == "F9IdentityRecord" and rec["version"] == C.F9_VERSION and rec["contract_sha256"] == C.F9_CONTRACT_SHA256
    assert sorted(rec["terrains"]) == sorted(C.F9_TERRAINS) and sorted(rec["arms"]) == sorted(f"{t}.{c}" for t, c in C.F9_ARMS)
    assert sorted(rec["families"]) == ["TA.shared", "TB.H", "TB.P", "TC.shared", "TD-1-2.shared", "TD-1-4.shared", "TD-4-2.shared", "TD-4-4.shared"]
    assert rec["schema"] == 2 and sorted(rec["arrays"]) == sorted(I.array_files())
    assert len(rec["arrays"]) == 3 * 8 + 8 and all(isinstance(h, str) and len(h) == 64 for h in rec["arrays"].values())
    assert I.canonical_json(I.build_identity_record()) == I.canonical_json(rec)       # a bare record is the bundle's record
    assert rec["arms"]["T0.P"]["family"] == "empty: no eligible contour" and rec["arms"]["T0.P"]["omega_key"] is None
    for name, _lat in C.F9_SAME_FAMILY_LATENT:
        sf = rec["same_family"][name]
        assert sf["arrays_identical"] and sf["masks_identical"] and sf["masks_sha256"] == rec["families"][f"{name}.shared"]["masks_sha256"]
        assert rec["arms"][f"{name}.P"]["omega_key"] == rec["arms"][f"{name}.H"]["omega_key"] == f"{name}.shared"
        for comp in C.F9_COMPOSITIONS: assert rec["arms"][f"{name}.{comp}"]["relation_to_shared_array"]["largest_fall"] <= 1e-12
    assert "TB" not in rec["same_family"] and rec["arms"]["TB.P"]["omega_key"] == "TB.P" and rec["arms"]["TB.H"]["omega_key"] == "TB.H"
    for name in ("TD-1-2", "TD-1-4", "TD-4-2", "TD-4-4"): assert rec["terrains"][name]["core"]["cells"] == 2000
    assert rec["terrains"]["TD-1-2"]["core"]["mask_sha256"] == rec["terrains"]["TD-1-4"]["core"]["mask_sha256"]
    json.dumps(rec, allow_nan=False)


def test_bundle_round_trips_and_the_record_follows_from_the_stored_arrays(bundle):
    d, rec = bundle
    with open(os.path.join(d, I.RECORD_NAME), "rb") as fh: raw = fh.read()
    assert raw == I.canonical_json(rec) and raw.endswith(b"\n") and b"\r" not in raw and I.record_identity(rec) == hashlib.sha256(raw).hexdigest()
    rec2, arrays = I.load_bundle(d)
    assert rec2 == json.loads(raw) and len(arrays) == 32
    for name in C.F9_TERRAINS:
        for k, b in enumerate(("v", "u", "r")): assert np.array_equal(arrays[f"bases/{name}.{b}.f64"], T.bases(name)[k])
    assert np.array_equal(arrays["omega/TB.H.f64"], T.comparison_array("TB", "H"))
    assert I.verify_bundle_deep(d) == rec2
    assert I.verify_bundle_deep(d, float_rtol=C.F9_SPR_RECOMPUTE_RTOL)["version"] == C.F9_VERSION
    assert np.array_equal(arrays["omega/TC.shared.f64"], I.derived_omega("TC", "H", *T.bases("TC")))
    cmp_ = I.compare_bundles(d, d)
    assert cmp_["record_a_sha256"] == cmp_["record_b_sha256"] == I.record_identity(rec)
    assert cmp_["largest_base_deviation"] == 0.0 and cmp_["base_arrays_bit_identical"] and cmp_["all_families_same_masks"] and cmp_["spr_within_tolerance"]
    with pytest.raises(C.F9ConfigError): I.write_bundle(d)                    # a record is never overwritten


def test_a_second_build_gives_the_same_record(bundle, tmp_path):
    d, rec = bundle
    rec2 = I.write_bundle(str(tmp_path / "again"))
    assert I.canonical_json(rec2) == I.canonical_json(rec)


def _mutated(src, dst, mutate):
    """A copy of a bundle with its record changed by `mutate(record, directory)` and re-serialized canonically."""
    shutil.copytree(src, dst)
    rp = os.path.join(dst, I.RECORD_NAME)
    with open(rp, "rb") as fh: r = json.loads(fh.read())
    mutate(r, dst)
    with open(rp, "wb") as fh: fh.write(I.canonical_json(r))
    return dst


def _refused(fn, *a, **k):
    try: fn(*a, **k)
    except C.F9ConfigError: return True
    return False


def test_byte_and_form_tampering_is_refused_by_the_loader(bundle, tmp_path):
    d, rec = bundle
    t1 = str(tmp_path / "t1"); shutil.copytree(d, t1)                         # one array bit changed
    p = os.path.join(t1, "bases", "TA.v.f64"); b = bytearray(open(p, "rb").read()); b[0] ^= 1; open(p, "wb").write(bytes(b))
    assert _refused(I.load_bundle, t1)
    t4 = str(tmp_path / "t4"); shutil.copytree(d, t4)                         # not canonical JSON
    raw = open(os.path.join(t4, I.RECORD_NAME), "rb").read(); open(os.path.join(t4, I.RECORD_NAME), "wb").write(raw.replace(b"\n", b"\r\n"))
    assert _refused(I.load_bundle, t4)
    t5 = _mutated(d, str(tmp_path / "t5"), lambda r, _d: r.__setitem__("declaration_sha256", "0" * 64))        # another declaration
    assert _refused(I.load_bundle, t5)
    t6 = _mutated(d, str(tmp_path / "t6"), lambda r, _d: r["arrays"].pop("omega/TB.H.f64"))                    # an array not named
    assert _refused(I.load_bundle, t6)
    t7 = _mutated(d, str(tmp_path / "t7"), lambda r, _d: r["arrays"].__setitem__("omega/EXTRA.f64", "0" * 64))  # an undeclared array named
    assert _refused(I.load_bundle, t7)
    t8 = _mutated(d, str(tmp_path / "t8"), lambda r, _d: r.__setitem__("schema", 1))
    assert _refused(I.load_bundle, t8)


def _empty_coverage(r, d):
    r["arms"] = {}; r["families"] = {}; r["same_family"] = {}


def _wrong_gain(r, d):
    r["arms"]["TB.H"]["g_spec"] *= 2.0


def _wrong_comparison(r, d):
    raw = open(os.path.join(d, "omega", "TB.P.f64"), "rb").read()
    open(os.path.join(d, "omega", "TB.H.f64"), "wb").write(raw)
    r["arrays"]["omega/TB.H.f64"] = hashlib.sha256(raw).hexdigest()
    r["families"]["TB.H"] = json.loads(json.dumps(r["families"]["TB.P"]))


def _wrong_arm_binding(r, d):
    r["arms"]["TC.H"]["omega_key"] = "TB.P"


L2_R2_CASES = {"empty_coverage": _empty_coverage, "wrong_gain": _wrong_gain, "wrong_comparison": _wrong_comparison, "wrong_arm_binding": _wrong_arm_binding}


@pytest.mark.parametrize("case", sorted(L2_R2_CASES))
def test_inconsistent_records_are_refused_l2_m1_round1_r2(bundle, tmp_path, case):
    """L2 M1 round 1, R2: each of L2's four records is canonical JSON whose array hashes hold, so the loader (form and
    bytes only) accepts it; the semantic verifier must refuse each one separately. The unchanged bundle is the control
    (`test_bundle_round_trips_and_the_record_follows_from_the_stored_arrays` verifies it deeply)."""
    d, rec = bundle
    t = _mutated(d, str(tmp_path / case), L2_R2_CASES[case])
    I.load_bundle(t)
    assert _refused(I.verify_bundle_deep, t)
    assert _refused(I.verify_bundle_deep, t, float_rtol=C.F9_SPR_RECOMPUTE_RTOL)
    if case == "wrong_comparison":
        assert _refused(I.compare_bundles, t, d)                              # the comparison takes verified bundles only


MORE_SEMANTIC_CASES = {
    "one_arm_missing": lambda r, d: r["arms"].pop("TD-4-4.H"),
    "an_extra_arm": lambda r, d: r["arms"].__setitem__("T0.H", json.loads(json.dumps(r["arms"]["T0.P"]))),
    "one_family_missing": lambda r, d: r["families"].pop("TD-1-4.shared"),
    "same_family_entry_missing": lambda r, d: r["same_family"].pop("TC"),
    "same_family_assertion_false": lambda r, d: r["same_family"]["TA"].__setitem__("masks_identical", False),
    "tb_listed_as_same_family": lambda r, d: r["same_family"].__setitem__("TB", json.loads(json.dumps(r["same_family"]["TA"]))),
    "arm_terrain_field_wrong": lambda r, d: r["arms"]["TA.P"].__setitem__("terrain", "TC"),
    "arm_composition_field_wrong": lambda r, d: r["arms"]["TA.P"].__setitem__("composition", "H"),
    "t0_given_a_family": lambda r, d: r["arms"]["T0.P"].__setitem__("omega_key", "TA.shared"),
    "spr_off_by_1e-6": lambda r, d: r["arms"]["TA.P"].__setitem__("spr", r["arms"]["TA.P"]["spr"] * (1 + 1e-6)),
    "family_count_wrong": lambda r, d: r["families"]["TB.H"].__setitem__("n_levels", 51),
    "component_identity_wrong": lambda r, d: r["families"]["TD-4-2.shared"].__setitem__("components_sha256", "0" * 64),
    "core_cells_wrong": lambda r, d: r["terrains"]["TD-1-2"]["core"].__setitem__("cells", 1999),
    "q_wrong": lambda r, d: r.__setitem__("q", 0.2),
    "levels_wrong": lambda r, d: r["levels_micro"].pop(),
    "int_where_a_float_belongs": lambda r, d: r["arms"]["T0.P"].__setitem__("index_min", 1),
    "environment_not_strings": lambda r, d: r["environment"].__setitem__("python", 3),
    "an_extra_top_level_field": lambda r, d: r.__setitem__("note", "x"),
}


@pytest.mark.parametrize("case", sorted(MORE_SEMANTIC_CASES))
def test_the_record_must_equal_what_the_stored_arrays_give(bundle, tmp_path, case):
    d, rec = bundle
    t = _mutated(d, str(tmp_path / "m"), MORE_SEMANTIC_CASES[case])
    I.load_bundle(t)                                                          # form and bytes hold in every case
    assert _refused(I.verify_bundle_deep, t, float_rtol=C.F9_SPR_RECOMPUTE_RTOL)   # refused even at the looser, cross-machine tolerance


def test_float_tolerance_is_for_another_machine_only(bundle, tmp_path):
    d, rec = bundle
    def nudge(r, _d):
        a = r["arms"]["TC.P"]; a["spr"] *= (1 + 1e-11); a["g_spec"] = r["q"] / (C.F9_DT * a["spr"])
    t = _mutated(d, str(tmp_path / "n"), nudge)
    assert _refused(I.verify_bundle_deep, t)                                  # the writing machine must reproduce its floats exactly
    assert I.verify_bundle_deep(t, float_rtol=C.F9_SPR_RECOMPUTE_RTOL)["arms"]["TC.P"]["spr"] != rec["arms"]["TC.P"]["spr"]
    for bad in (1e-6, 1e-12, 1, True, None, 2 * C.F9_SPR_RECOMPUTE_RTOL):       # a caller cannot choose a tolerance
        assert _refused(I.verify_bundle_deep, d, float_rtol=bad)
        assert _refused(I.compare_bundles, d, d, float_rtol=bad)


def _spr_nudge(arm, factor, coherent):
    def mutate(r, _d):
        a = r["arms"][arm]; a["spr"] = a["spr"] * (1.0 + factor)
        if coherent: a["g_spec"] = r["q"] / (C.F9_DT * a["spr"])
    return mutate


# L2 M1 round 2, §4: (arm, nudge, coherent g_spec, accepted on another machine). The two refused rows are L2's witnesses.
L2_ROUND2_SPECTRAL = {
    "within_bound_coherent": ("TB.P", 0.9e-9, True, True),
    "l2_spectral_only_1.004e-9": ("TB.P", 1.004e-9, False, False),
    "l2_coherent_pair_1.0003e-9": ("TB.P", 1.0003e-9, True, False),
}


@pytest.mark.parametrize("case", sorted(L2_ROUND2_SPECTRAL))
def test_spectral_tolerance_is_pure_relative_l2_m1_round2(bundle, tmp_path, case):
    """L2 M1 round 2, §4: on another machine a recorded spectral radius is held to 1e-9 RELATIVE with nothing added
    (contract §2.8). L2's two records lie beyond it and inside the former `rtol*value + 1e-12`; both must be refused
    with the typed discrepancy, and a record inside the bound is the control."""
    d, rec = bundle
    arm, factor, coherent, accepted = L2_ROUND2_SPECTRAL[case]
    t = _mutated(d, str(tmp_path / "s"), _spr_nudge(arm, factor, coherent))
    with open(os.path.join(t, I.RECORD_NAME), "rb") as fh: stated = json.loads(fh.read())["arms"][arm]["spr"]
    ref = rec["arms"][arm]["spr"]
    rel = abs(stated - ref) / min(stated, ref)
    old_allowance = C.F9_SPR_RECOMPUTE_RTOL * max(stated, ref) + C.F9_CROSS_PLATFORM_TOL
    assert abs(stated - ref) <= old_allowance                                 # every case sat inside the round-2 allowance
    assert (rel <= C.F9_SPR_RECOMPUTE_RTOL) == accepted
    assert _refused(I.verify_bundle_deep, t)                                  # exact mode refuses all three
    if accepted:
        assert I.verify_bundle_deep(t, float_rtol=C.F9_SPR_RECOMPUTE_RTOL)["arms"][arm]["spr"] == stated
    else:
        with pytest.raises(I.F9SpectralDiscrepancy) as info: I.verify_bundle_deep(t, float_rtol=C.F9_SPR_RECOMPUTE_RTOL)
        e = info.value
        assert isinstance(e, C.F9ConfigError) and e.arm == arm and e.stated == stated and e.recomputed == ref and e.relative == rel
        assert _refused(I.compare_bundles, t, d) and _refused(I.compare_bundles, d, t)


def test_gain_must_follow_from_the_records_own_q_and_spr(bundle, tmp_path):
    """On another machine g_spec has no tolerance of its own: it is q/(dt*spr) of the record's own values, exactly."""
    d, rec = bundle
    def incoherent(r, _d):
        a = r["arms"]["TC.P"]; a["spr"] *= (1 + 1e-11); a["g_spec"] = math.nextafter(r["q"] / (C.F9_DT * a["spr"]), math.inf)
    t = _mutated(d, str(tmp_path / "g1"), incoherent)
    assert _refused(I.verify_bundle_deep, t) and _refused(I.verify_bundle_deep, t, float_rtol=C.F9_SPR_RECOMPUTE_RTOL)
    def gain_alone(r, _d): r["arms"]["TA.H"]["g_spec"] = math.nextafter(r["arms"]["TA.H"]["g_spec"], 0.0)
    t = _mutated(d, str(tmp_path / "g2"), gain_alone)
    assert _refused(I.verify_bundle_deep, t) and _refused(I.verify_bundle_deep, t, float_rtol=C.F9_SPR_RECOMPUTE_RTOL)


def test_a_last_place_difference_in_q_is_another_machines_libm(bundle, tmp_path):
    """q = 1 - exp(-0.2) may differ in the last place of exp between platforms. A record written with such a q, and
    gains that follow from it, verifies on another machine and not on the writing machine."""
    d, rec = bundle
    def other_libm(r, _d):
        r["q"] = 1.0 - math.nextafter(1.0 - r["q"], 0.0)
        for a in r["arms"].values(): a["g_spec"] = r["q"] / (C.F9_DT * a["spr"])
    t = _mutated(d, str(tmp_path / "q"), other_libm)
    assert _refused(I.verify_bundle_deep, t)
    assert I.verify_bundle_deep(t, float_rtol=C.F9_SPR_RECOMPUTE_RTOL)["q"] != rec["q"]


def _with(rec, path, value):
    r = json.loads(json.dumps(rec)); node = r
    for k in path[:-1]: node = node[k]
    node[path[-1]] = value
    return r


def test_each_float_takes_the_rule_of_its_own_quantity(bundle):
    """The comparator on another machine, field by field (no bundle is rewritten here; `_same` compares a stated record
    with the recomputed one). No rule borrows another's allowance."""
    d, rec = bundle
    same = lambda r, cross: not _refused(I._same, r, rec, cross)
    assert same(rec, False) and same(rec, True)
    for arm, entry in rec["arms"].items():                                    # spr: pure relative, on all fifteen arms
        ref = entry["spr"]
        inside, outside = ref * (1.0 + 0.999e-9), ref * (1.0 + 1.001e-9)
        assert abs(outside - ref) <= C.F9_SPR_RECOMPUTE_RTOL * max(outside, ref) + C.F9_CROSS_PLATFORM_TOL    # the round-2 rule took it
        assert same(_with(rec, ("arms", arm, "spr"), inside), True) and not same(_with(rec, ("arms", arm, "spr"), inside), False)
        with pytest.raises(I.F9SpectralDiscrepancy): I._same(_with(rec, ("arms", arm, "spr"), outside), rec, True)
        with pytest.raises(I.F9SpectralDiscrepancy): I._same(_with(rec, ("arms", arm, "spr"), ref * (1.0 - 1.001e-9)), rec, True)
        with pytest.raises(I.F9SpectralDiscrepancy): I._same(_with(rec, ("arms", arm, "spr"), -ref), rec, True)
    q, eta = rec["q"], rec["eta0"]                                             # q, eta0: two units in the last place of the libm result
    u = math.ulp(1.0 - q)
    assert same(_with(rec, ("q",), q + 2 * u), True) and not same(_with(rec, ("q",), q + 2 * u), False)
    assert not same(_with(rec, ("q",), q + 4 * u), True) and not same(_with(rec, ("q",), q * (1 + 1e-12)), True)
    v = math.ulp(eta)
    assert same(_with(rec, ("eta0",), eta - 2 * v), True) and not same(_with(rec, ("eta0",), eta - 2 * v), False)
    assert not same(_with(rec, ("eta0",), eta + 4 * v), True) and not same(_with(rec, ("eta0",), eta * (1 + 1e-12)), True)
    sh = rec["terrains"]["TB"]["product_variance_shares"]                     # TB's descriptive variance figures: 1e-12 absolute
    for k in ("x", "y", "additive_residual"):
        p = ("terrains", "TB", "product_variance_shares", k)
        assert same(_with(rec, p, sh[k] + 0.5e-12), True) and not same(_with(rec, p, sh[k] + 0.5e-12), False)
        assert not same(_with(rec, p, sh[k] + 2e-12), True)
    exact = [("terrains", "TB", "base_max"), ("terrains", "TB", "cross_fall", "H_along_P"), ("terrains", "TD-1-2", "core", "least_distance_of_a_centre_to_the_edge"),
             ("arms", "TA.P", "index_min"), ("arms", "TC.H", "index_max"), ("arms", "TA.H", "relation_to_shared_array", "largest_spread_within_a_level"),
             ("families", "TB.P", "level_min"), ("families", "TC.shared", "level_max"), ("families", "TD-1-4.shared", "min_level_gap")]
    for p in exact:                                                           # every other float: equal, on any machine
        node = rec
        for k in p: node = node[k]
        assert isinstance(node, float) and node != 0.0
        assert not same(_with(rec, p, math.nextafter(node, math.inf)), True) and not same(_with(rec, p, math.nextafter(node, math.inf)), False)
    floats = []                                                               # and the rule table names exactly the fields it should
    def walk(x, path):
        if isinstance(x, dict):
            for k, y in x.items(): walk(y, path + (k,))
        elif isinstance(x, list):
            for i, y in enumerate(x): walk(y, path + (f"[{i}]",))
        elif isinstance(x, float): floats.append(path)
    walk(rec, ())
    ruled = sorted(p for p in floats if I._float_rule(p) != "exact")
    want = sorted([("q",), ("eta0",)] + [("arms", a, f) for a in rec["arms"] for f in ("spr", "g_spec")]
                  + [("terrains", "TB", "product_variance_shares", k) for k in ("x", "y", "additive_residual")])
    assert ruled == want and len(floats) > len(want)


def _rewrite_array(directory, record, rel, arr):
    raw = T.serialize(arr)
    with open(I._resolve(directory, rel), "wb") as fh: fh.write(raw)
    record["arrays"][rel] = hashlib.sha256(raw).hexdigest()


def test_stored_bases_must_be_the_declared_terrains(bundle, tmp_path):
    """§3.4 step 5 inside the verifier: bases whose own hashes hold but which are not the declared terrain are refused,
    whether the record's other fields were left alone or rebuilt consistently from the altered bases."""
    d, rec = bundle
    v, u, r_ = T.bases("TC")
    def shifted(r, directory):
        _rewrite_array(directory, r, "bases/TC.u.f64", np.clip(u + 1e-9, 0.0, 1.0))
    t = _mutated(d, str(tmp_path / "s1"), shifted)
    I.load_bundle(t); assert _refused(I.verify_bundle_deep, t) and _refused(I.verify_bundle_deep, t, float_rtol=C.F9_SPR_RECOMPUTE_RTOL)
    def coherent_but_wrong(r, directory):                                      # a self-consistent record of a DIFFERENT terrain
        bases = I.machine_bases(); bases["TC"] = (v, np.ascontiguousarray(u[::-1].copy()), r_)
        new = I.record_from_bases(bases, r["environment"])
        _rewrite_array(directory, new, "bases/TC.u.f64", bases["TC"][1])
        _rewrite_array(directory, new, "omega/TC.shared.f64", I.derived_omega("TC", "P", *bases["TC"]))
        r.clear(); r.update(new)
    t = _mutated(d, str(tmp_path / "s2"), coherent_but_wrong)
    I.load_bundle(t); assert _refused(I.verify_bundle_deep, t)
    def within_tolerance(r, directory):                                        # 1e-13 away: inside §3.4 step 5, so the bases pass ...
        bases = I.machine_bases(); bases["TC"] = (v, np.clip(u + 1e-13, 0.0, 1.0), r_)
        new = I.record_from_bases(bases, r["environment"])
        _rewrite_array(directory, new, "bases/TC.u.f64", bases["TC"][1])
        _rewrite_array(directory, new, "omega/TC.shared.f64", I.derived_omega("TC", "P", *bases["TC"]))
        r.clear(); r.update(new)
    t = _mutated(d, str(tmp_path / "s3"), within_tolerance)
    assert I.verify_bundle_deep(t)["arrays"]["bases/TC.u.f64"] != rec["arrays"]["bases/TC.u.f64"]   # ... and its own record verifies
    c = I.compare_bundles(d, t)
    assert 0.0 < c["largest_base_deviation"] <= 1e-12 and c["largest_base_deviation_array"] == "bases/TC.u.f64" and not c["base_arrays_bit_identical"]


def test_record_from_bases_refuses_bases_that_break_a_declared_relation():
    bases = I.machine_bases(); env = I.environment()
    for name, breaker in (("T0", lambda v, u, r: (v, u, np.full((L, L), 0.7))),
                          ("TA", lambda v, u, r: (v, u, np.clip(r + 1e-6, 0, 1))),
                          ("TD-1-2", lambda v, u, r: tuple(np.roll(x, 1, 0) for x in (v, u, r)))):
        b = dict(bases); b[name] = breaker(*bases[name])
        assert _refused(I.record_from_bases, b, env)
    b = dict(bases); b.pop("TC"); assert _refused(I.record_from_bases, b, env)
    b = dict(bases); b["TB"] = tuple(x.astype(np.float32) for x in bases["TB"]); assert _refused(I.record_from_bases, b, env)


def test_array_paths_are_declared_literals():
    paths = list(I.array_files())
    assert len(paths) == len(set(paths)) == 32 and all("\\" not in p and p.count("/") == 1 and p.endswith(".f64") for p in paths)
    assert paths[:3] == ["bases/T0.v.f64", "bases/T0.u.f64", "bases/T0.r.f64"] and "omega/TA.shared.f64" in paths and "omega/TB.P.f64" in paths
    assert I.family_keys() == ("TA.shared", "TB.P", "TB.H", "TC.shared", "TD-1-2.shared", "TD-1-4.shared", "TD-4-2.shared", "TD-4-4.shared")
    assert I.omega_key("T0", "P") is None and I.omega_key("TC", "H") == "TC.shared" and I.omega_key("TB", "H") == "TB.H"
    for bad in ("../x", "a//b", "/abs", "a/../b"):
        with pytest.raises(C.F9ConfigError): I._resolve("out", bad)


# contract §3.4 step 3 and §5.5 step 5: registered family sizes and distinct values before rounding — CONTAINER values, provisional
CONTAINER_SIZES = {"TA.shared": (1300, 2221), "TC.shared": (1180, 1389), "TD-1-2.shared": (681, 861), "TD-1-4.shared": (920, 920),
                   "TD-4-2.shared": (250, 250), "TD-4-4.shared": (250, 250), "TB.P": (2600, 3840), "TB.H": (50, 59)}


def test_container_values_are_reported(bundle, capsys):
    """Reports, for the record of the machine running the suite, whether the registered family sizes equal the frozen
    contract's provisional container values. Asserts nothing about the sizes (see the module docstring); asserts only
    that every declared family is present in the record."""
    d, rec = bundle
    report = {k: {"here": (rec["families"][k]["n_levels"], rec["families"][k]["distinct_values_before_rounding"]), "contract": v,
                  "equal": (rec["families"][k]["n_levels"], rec["families"][k]["distinct_values_before_rounding"]) == v} for k, v in CONTAINER_SIZES.items()}
    with capsys.disabled():
        print("\nF9 M1 registered family sizes (here vs contract, provisional):", json.dumps(report, sort_keys=True))
    assert sorted(report) == sorted(rec["families"])


# ======================= nothing in e1 or f8 is touched =======================
UNTOUCHED = "c80d494aea4e5e452b4a96536f0bc68515918e4ac8c7f37e84d66bad7c7a3289"


def test_e1_and_f8_are_byte_unchanged():
    """The placed e1 and f8 packages and the frozen package root, as LF blobs, hash to their identities at the commit this
    module was built against (b2a5674). M1 imports from the root and adds a package beside them; it edits none of them."""
    h = hashlib.sha256()
    names = []
    for sub in ("", "e1", "f8", "gates"):
        d = os.path.join(PKG, sub)
        for fn in sorted(os.listdir(d)):
            if fn.endswith(".py"): names.append((sub + "/" + fn if sub else fn, os.path.join(d, fn)))
    for rel, path in names:
        h.update(rel.encode()); h.update(bytes.fromhex(_sha_lf(path)))
    assert h.hexdigest() == UNTOUCHED
