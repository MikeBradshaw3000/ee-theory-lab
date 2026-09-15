"""tests/test_gate_b_m1.py — Gate B harness module 1: reference loader, comparators, stub.
Every check has a negative built to break it (pessimistic-on-passing)."""
import os
import numpy as np
import pytest

from mfa_instrument.gates.gate_b import reference as R
from mfa_instrument.gates.gate_b.environment import check_environment
from mfa_instrument.gates.gate_b.comparators import (raw_bits_differ, compare_float64,
                                                    scalar_bits_equal, state_mismatches, ComparatorError)
from mfa_instrument.gates.gate_b.stub import FrozenSequenceGenerator, StubError
from mfa_instrument.rng import DynamicsStream, SeedRegistry
from mfa_instrument.config import RunConfig, InitConfig, DynamicsConstants
from mfa_instrument.init import initialize
from mfa_instrument.dynamics import Dynamics

PIN = os.environ.get("MFA_PINNED_REPO_ROOT")
needs_pin = pytest.mark.skipif(not PIN, reason="MFA_PINNED_REPO_ROOT unset (no pinned clone)")


# ---------------- reference loader ----------------
@needs_pin
def test_reference_extraction_load_verifies_and_exposes_symbols():
    r = R.load_pinned_reference(PIN, "EXTRACTION", "PROVISIONAL")
    assert r.provenance.commit_verified == "4d9a622" and r.provenance.observed_sha256 == R.EXPECTED_SHA256
    assert r.provenance.load_mode == "EXTRACTION" and r.module is None
    for s in R.REQUIRED_SYMBOLS:
        assert s in r.ns
    assert scalar_bits_equal(r.LAMBDA, 0.40) and scalar_bits_equal(r.LOGIT_L, float(np.log(0.4 / 0.6)))
    assert len(r.KAPPA_MAP) == 9 and r.u_t_for("cm1", 0.25, 0.0, 1) == 0.125

@needs_pin
def test_reference_step_matches_hand_case():
    r = R.load_pinned_reference(PIN)
    grid = np.zeros((4, 4), dtype=int); grid[1, 1] = 1
    rand = np.full((4, 4), 0.5)
    nxt, p = r.step_tcop_core(grid, 0.0, 0.0, rand)
    assert p.dtype == np.float64 and nxt.dtype.kind in "iu"
    # kappa=0, u_t=0: every cell's p_become = sigmoid(LOGIT_L) = LAMBDA exactly, bit for bit;
    # rand 0.5 >= 0.4 everywhere: no inactive cell becomes, the one active cell dies.
    assert raw_bits_differ(p, np.full((4, 4), r.LAMBDA)) == 0
    assert nxt.sum() == 0
    # and a rand below LAMBDA flips both outcomes: becomes everywhere, survivor survives
    nxt2, _ = r.step_tcop_core(grid, 0.0, 0.0, np.full((4, 4), 0.39))
    assert nxt2.sum() == 16

def test_reference_refuses_authoritative_in_extraction_mode(tmp_path):
    with pytest.raises(R.ReferenceError, match="AUTHORITATIVE"):
        R.load_pinned_reference(str(tmp_path), "EXTRACTION", "AUTHORITATIVE")

def test_reference_refuses_absent_pinned_mirror(tmp_path):
    with pytest.raises(R.ReferenceError, match="mirror absent"):
        R.load_pinned_reference(str(tmp_path))

def _arm_execution_sentinel(monkeypatch, mode):
    """A sentinel on the execution path ACTUALLY exercised by `mode` (L2 M1-2): FULL executes through
    exec_verified_bytes; EXTRACTION compiles its line regions with a filename ending in ':extraction>'."""
    if mode == "FULL":
        monkeypatch.setattr(R, "exec_verified_bytes", lambda *a, **k: (_ for _ in ()).throw(AssertionError("FULL must not execute")))
    else:
        import builtins
        real_compile = builtins.compile
        def guarded(src, filename, *a, **k):
            if isinstance(filename, str) and filename.endswith(":extraction>"):
                raise AssertionError("EXTRACTION must not compile/execute")
            return real_compile(src, filename, *a, **k)
        monkeypatch.setattr(builtins, "compile", guarded)

@needs_pin
@pytest.mark.parametrize("mode", ["EXTRACTION", pytest.param("FULL", marks=pytest.mark.skipif(
    not (PIN and check_environment(PIN).conforms), reason="canonical environment required"))])
def test_reference_refuses_blob_digest_mismatch_before_any_execution(monkeypatch, mode):
    """TRUE identity negative (L2 ruling 3.3): the git BLOB itself is altered by one byte (via the
    blob-read helper); the loader must refuse with digest FAILED naming the blob, and the execution
    path of the exercised MODE must not be reached. Worktree tampering is no longer an identity event."""
    real = R.read_pinned_blob
    def altered(root):
        b = bytearray(real(root)); b[-2] ^= 0x01; return bytes(b)
    monkeypatch.setattr(R, "read_pinned_blob", altered)
    _arm_execution_sentinel(monkeypatch, mode)
    label = "AUTHORITATIVE" if mode == "FULL" else "PROVISIONAL"
    with pytest.raises(R.ReferenceError, match=r"digest FAILED: blob 4d9a622"):
        R.load_pinned_reference(PIN, mode, label)
    monkeypatch.undo()
    monkeypatch.setattr(R, "EXPECTED_SHA256", "0" * 64)
    _arm_execution_sentinel(monkeypatch, mode)
    with pytest.raises(R.ReferenceError, match="digest FAILED"):
        R.load_pinned_reference(PIN, mode, label)

def test_extraction_execution_sentinel_is_live(monkeypatch):
    """The EXTRACTION sentinel must itself be shown to fire when the extraction path IS reached."""
    _arm_execution_sentinel(monkeypatch, "EXTRACTION")
    with pytest.raises(AssertionError, match="EXTRACTION must not"):
        compile("x = 1", "<gate_b_test:extraction>", "exec")

def test_reference_refuses_unknown_mode_and_label(tmp_path):
    with pytest.raises(R.ReferenceError, match="load_mode"):
        R.load_pinned_reference(str(tmp_path), "PARTIAL")
    with pytest.raises(R.ReferenceError, match="label"):
        R.load_pinned_reference(str(tmp_path), "EXTRACTION", "CERTIFIED")


# ---------------- comparators ----------------
def test_raw_bits_signed_zero_discriminated():
    a = np.array([0.0, 1.0]); b = np.array([-0.0, 1.0])
    assert np.array_equal(a, b)                      # the weaker comparator passes
    assert raw_bits_differ(a, b) == 1                # the frozen one does not

def test_raw_bits_one_ulp_counted_exactly():
    a = np.random.default_rng(0).random((5, 5)); b = a.copy(); b[2, 3] = np.nextafter(b[2, 3], 1.0)
    c = compare_float64(a, b)
    assert c.differing_cells == 1 and not c.bit_exact and c.allclose_diagnostic is True

def test_raw_bits_refuses_dtype_and_shape_mismatch():
    with pytest.raises(ComparatorError, match="float64"):
        raw_bits_differ(np.zeros(3, np.float32), np.zeros(3))
    with pytest.raises(ComparatorError, match="shape"):
        raw_bits_differ(np.zeros((2, 2)), np.zeros((4,)))

def test_state_compare_exact_and_dtype_strict():
    anc = np.array([[1, 0], [0, 1]]); cand = anc.astype(bool)
    assert state_mismatches(cand, anc) == 0
    cand2 = cand.copy(); cand2[0, 0] = False
    assert state_mismatches(cand2, anc) == 1
    with pytest.raises(ComparatorError, match="boolean"):
        state_mismatches(anc, anc)                   # candidate as int is refused
    with pytest.raises(ComparatorError, match="integer"):
        state_mismatches(cand, anc.astype(float))
    with pytest.raises(ComparatorError, match="binary"):
        state_mismatches(cand, np.array([[2, 0], [0, 1]]))


# ---------------- counted stub ----------------
def _grids(n, gs=4, seed=1):
    g = np.random.default_rng(seed)
    return [g.random((gs, gs)) for _ in range(n)]

def test_stub_returns_declared_grids_in_order_immutably():
    gs = _grids(2); s = FrozenSequenceGenerator(gs, 4)
    a = s.random(size=(4, 4)); s.next_tick(); b = s.random(size=(4, 4))
    assert np.array_equal(a, gs[0]) and np.array_equal(b, gs[1]) and s.total_draws == 2
    s.assert_consumed()

def test_stub_refuses_wrong_shape_second_draw_exhaustion_and_surplus():
    s = FrozenSequenceGenerator(_grids(1), 4)
    with pytest.raises(StubError, match="shape"):
        s.random(size=(4, 5))
    s.random(size=(4, 4))
    with pytest.raises(StubError, match="second full-grid draw"):
        s.random(size=(4, 4))
    s.next_tick()
    with pytest.raises(StubError, match="exhausted"):
        s.random(size=(4, 4))
    s2 = FrozenSequenceGenerator(_grids(2), 4); s2.random(size=(4, 4))
    with pytest.raises(StubError, match="not fully consumed"):
        s2.assert_consumed()

def test_stub_rejects_grid_of_wrong_shape_at_construction():
    with pytest.raises(StubError):
        FrozenSequenceGenerator([np.zeros((3, 4))], 4)

def test_stub_drives_candidate_through_public_dispatch_one_draw_per_tick():
    """The instrument's own construction path (DynamicsStream) accepts the stub; a B step via the
    PUBLIC Dynamics.step consumes exactly one grid, and the sink's rand_grid is that grid."""
    gs = 6
    cfg = RunConfig(seed=5, rule_mode="become_survive", grid_scale=gs, ticks=2,
                    init=InitConfig(scheme="fixed_count", fixed_count=7),
                    constants=DynamicsConstants(logit_l=float(np.log(0.4/0.6)), kappa=0.4221, p_survive=0.4),
                    drive_schedule=((0, 0.25),))
    state = initialize(cfg.init, gs, SeedRegistry(5).dynamics())
    grids = _grids(2, gs, seed=9)
    stub = FrozenSequenceGenerator(grids, gs)
    d = Dynamics(cfg, state, DynamicsStream(generator=stub))
    captured = {}
    d.step(lambda tick, fields: captured.update({"rand": fields["rand_grid"].copy(), "tick": tick}))
    assert stub.total_draws == 1 and captured["tick"] == 0 and np.array_equal(captured["rand"], grids[0])
    stub.next_tick(); d.step(None)
    assert stub.total_draws == 2; stub.assert_consumed()


# ====================== round-2 additions (L2 review of modules 1-2) ======================
import random as _pyrandom
import subprocess
from mfa_instrument.gates.gate_b import b1 as B1mod
from mfa_instrument.gates.gate_b.environment import check_environment, read_lock_pins, EnvironmentCheckError, EXPECTED_LOCK_SHA256
from mfa_instrument.gates.gate_b.comparators import scalar_bits

def test_exec_verified_bytes_executes_the_verified_object_not_the_path(tmp_path):
    """TOCTOU: after verification the path is changed; the executed namespace must reflect the
    VERIFIED bytes, proving the path is never reopened."""
    p = tmp_path / "m.py"
    p.write_bytes(b"VALUE = 'verified'\n")
    raw = p.read_bytes()
    p.write_bytes(b"VALUE = 'tampered'\n")          # change on disk AFTER the read that was hashed
    mod = R.exec_verified_bytes(raw, str(p), "gate_b_test_toctou")
    assert mod.VALUE == "verified" and mod.__file__ == str(p)

def test_exec_verified_bytes_restores_cwd_on_exception(tmp_path):
    before = os.getcwd()
    with pytest.raises(ZeroDivisionError):
        R.exec_verified_bytes(b"1/0\n", "x.py", "gate_b_test_cwd", cwd=str(tmp_path))
    assert os.getcwd() == before

@needs_pin
def test_reference_provenance_carries_measured_digest_realpath_and_worktree_status():
    r = R.load_pinned_reference(PIN)
    pv = r.provenance
    assert pv.observed_sha256 == R.EXPECTED_SHA256 and pv.observed_sha256 != ""
    assert pv.pinned_path == os.path.realpath(pv.pinned_path) and pv.pinned_root == os.path.realpath(PIN)
    assert isinstance(pv.worktree_dirty, bool) and isinstance(pv.source_file_dirty, bool)
    assert pv.git_object == "4d9a622:cycle3/wave_two/c3_w2_tcop.py" and "blob:" in pv.module_origin
    # platform-neutral (L2 M1-1): the mirror may legitimately differ from the blob on a default
    # checkout; the test asserts CONSISTENCY of the record, never equality to the blob
    assert pv.worktree_mirror_readable is True and isinstance(pv.worktree_mirror_sha256, str) and len(pv.worktree_mirror_sha256) == 64
    assert pv.worktree_mirror_matches_blob == (pv.worktree_mirror_sha256 == pv.observed_sha256)
    assert pv.observed_sha256 == R.EXPECTED_SHA256
    assert pv.python_version and pv.numpy_version == np.__version__

def _exact_byte_clone(dst):
    """A pinned clone whose checkout is byte-exact on every platform (no line-ending conversion)."""
    subprocess.run(["git", "-c", "core.autocrlf=false", "clone", "-q", "--shared", PIN, str(dst)], check=True)
    subprocess.run(["git", "-C", str(dst), "config", "core.autocrlf", "false"], check=True)
    subprocess.run(["git", "-C", str(dst), "checkout", "-q", "4d9a622"], check=True)

@needs_pin
def test_reference_dirty_worktree_is_reported_not_hidden(tmp_path):
    """Untracked file -> worktree_dirty True; the source path logically unmodified; identity is the
    blob (frozen digest) and the exact-byte mirror matches it (L2 ruling 3.1)."""
    root = tmp_path / "pin"; _exact_byte_clone(root)
    (root / "SCRATCH.txt").write_text("dirty")
    r = R.load_pinned_reference(str(root)); pv = r.provenance
    assert pv.worktree_dirty is True and pv.source_file_dirty is False
    assert pv.observed_sha256 == R.EXPECTED_SHA256 and pv.worktree_mirror_matches_blob is True
    assert pv.git_object == "4d9a622:cycle3/wave_two/c3_w2_tcop.py"

@needs_pin
def test_worktree_mirror_bytes_cannot_redefine_the_reference(tmp_path):
    """Platform/mirror independence (L2 ruling 3.2, portable): the checked-out mirror is replaced by
    its CRLF representation — the committed blob unchanged — and the loader must still verify the
    frozen digest, execute/extract the committed bytes, and report the mirror mismatch as provenance.
    This is the Windows first-contact event, reproduced on any host."""
    root = tmp_path / "pin"; _exact_byte_clone(root)
    mirror = root / R.PINNED_RELPATH
    lf = mirror.read_bytes(); assert b"\r\n" not in lf
    mirror.write_bytes(lf.replace(b"\n", b"\r\n"))
    r = R.load_pinned_reference(str(root)); pv = r.provenance
    assert pv.observed_sha256 == R.EXPECTED_SHA256                                   # identity: the blob
    assert pv.worktree_mirror_readable and pv.worktree_mirror_matches_blob is False
    assert pv.worktree_mirror_sha256 == "8add63cf469e225b35b86fd68e214921c5126ce3e89ff75af60505e858f2e8e2"   # the CRLF digest of record
    assert pv.worktree_dirty is True and isinstance(pv.source_file_dirty, bool)     # actual git statuses, whatever they are
    # execution reflects the committed blob: the extracted step reproduces the frozen LAMBDA and a known step
    assert scalar_bits_equal(r.LAMBDA, 0.40)
    grid = np.zeros((4, 4), dtype=int); grid[1, 1] = 1
    nxt, p = r.step_tcop_core(grid, 0.0, 0.0, np.full((4, 4), 0.5))
    assert raw_bits_differ(p, np.full((4, 4), r.LAMBDA)) == 0 and nxt.sum() == 0

@needs_pin
def test_reference_incomplete_symbols_raise_reference_error_not_keyerror(monkeypatch):
    monkeypatch.setattr(R, "REQUIRED_SYMBOLS", R.REQUIRED_SYMBOLS + ("NOT_A_SYMBOL",))
    with pytest.raises(R.ReferenceError, match="missing symbols \\['NOT_A_SYMBOL'\\]"):
        R.load_pinned_reference(PIN)

@pytest.mark.skipif(not (PIN and check_environment(PIN).conforms), reason="canonical environment required")
def test_reference_full_mode_loads_on_canonical_environment():
    r = R.load_pinned_reference(PIN, "FULL", "AUTHORITATIVE")
    assert r.module is not None and "execute_run" in r.ns and r.provenance.load_mode == "FULL"

def test_scalar_comparator_is_dtype_first_and_noncoercive():
    assert scalar_bits_equal(0.4, np.float64(0.4)) and not scalar_bits_equal(0.0, -0.0)   # signed zero
    with pytest.raises(ComparatorError, match="float64"):
        scalar_bits_equal(np.float32(0.4), 0.4)                                            # refused, not normalized
    with pytest.raises(ComparatorError, match="scalar required"):
        scalar_bits_equal(np.array([0.4]), 0.4)
    assert scalar_bits(0.4) == "0x3fd999999999999a"

def test_stub_returns_read_only_grids_and_refuses_bad_inputs():
    g = np.random.default_rng(3).random((4, 4))
    s = FrozenSequenceGenerator([g], 4)
    out = s.random(size=(4, 4))
    assert not out.flags.writeable
    with pytest.raises(ValueError):
        out[0, 0] = 0.1
    with pytest.raises(StubError, match="float64"):
        FrozenSequenceGenerator([g.astype(np.float32)], 4)
    bad = g.copy(); bad[1, 1] = np.nan
    with pytest.raises(StubError, match="nonfinite"):
        FrozenSequenceGenerator([bad], 4)
    bad = g.copy(); bad[1, 1] = 1.0
    with pytest.raises(StubError, match=r"\[0, 1\)"):
        FrozenSequenceGenerator([bad], 4)

@needs_pin
def test_reference_init_grid_restores_numpy_and_python_global_rng_states():
    r = R.load_pinned_reference(PIN)
    np.random.seed(777); _pyrandom.seed(999)
    np_before = np.random.get_state(); py_before = _pyrandom.getstate()
    g = B1mod.reference_init_grid(r, 42)
    assert g.sum() == 250 and g.shape == (50, 50)
    np_after = np.random.get_state(); py_after = _pyrandom.getstate()
    assert np_before[0] == np_after[0] and np.array_equal(np_before[1], np_after[1]) and np_before[2:] == np_after[2:]
    assert py_before == py_after
    # and the next draws from each global stream are what they would have been without the call
    assert np.random.rand() == np.random.RandomState(777).rand() and _pyrandom.random() == _pyrandom.Random(999).random()

@needs_pin
def test_reference_init_grid_restores_states_on_exception_path(monkeypatch):
    r = R.load_pinned_reference(PIN)
    np.random.seed(5); _pyrandom.seed(6)
    np_before = np.random.get_state(); py_before = _pyrandom.getstate()
    monkeypatch.setattr(np.random, "shuffle", lambda a: (_ for _ in ()).throw(RuntimeError("boom")))
    with pytest.raises(RuntimeError, match="boom"):
        B1mod.reference_init_grid(r, 42)
    assert np.array_equal(np_before[1], np.random.get_state()[1]) and _pyrandom.getstate() == py_before

def test_candidate_provenance_fails_closed_on_git_failure(tmp_path):
    sink = {}
    with pytest.raises(B1mod.ProvenanceError, match="candidate provenance") as ei:
        B1mod.candidate_provenance(str(tmp_path), sink)     # not a git repo -> never 'clean'
    assert ei.value.check == "candidate_git" and sink == {}  # nothing earned, nothing recorded

@needs_pin
def test_environment_check_reads_all_twenty_pins_bom_tolerant():
    pins, digest, _mirror = read_lock_pins(PIN)
    assert len(pins) == 20 and pins["numpy"] == "2.4.4" and pins["Mesa"] == "3.5.1" and "\ufeff" not in "".join(pins)
    rec = check_environment(PIN)
    assert rec.lock_sha256 == digest and len(rec.pins) == 20 and rec.python_build and rec.platform
    assert rec.conforms == (rec.venv_active and rec.python_conforms and all(v[2] for v in rec.pins.values()))


# ====================== round-3 additions ======================
@needs_pin
def test_lock_pins_read_from_git_blob_with_frozen_digest_and_mirror_check():
    """Platform-neutral (same principle as the reference tests, L2 M1-1): the lock blob is the
    identity; the worktree mirror's match status is a recorded fact that may be False on a default
    checkout. Assert consistency of the record, never equality to the blob."""
    pins, digest, mirror = read_lock_pins(PIN)
    assert digest == EXPECTED_LOCK_SHA256 and len(pins) == 20
    wt = os.path.join(PIN, "cycle3", "requirements.lock.txt")
    assert mirror == (open(wt, "rb").read() == __import__("subprocess").run(
        ["git", "-C", PIN, "show", "4d9a622:cycle3/requirements.lock.txt"], capture_output=True).stdout)

@needs_pin
def test_lock_mirror_match_is_true_on_an_exact_byte_clone(tmp_path):
    root = tmp_path / "pin"; _exact_byte_clone(root)
    pins, digest, mirror = read_lock_pins(str(root))
    assert digest == EXPECTED_LOCK_SHA256 and mirror is True

@needs_pin
def test_tampered_worktree_lock_cannot_redefine_environment(tmp_path):
    """One pin changed in the WORKTREE copy (twenty valid entries preserved): the blob at
    4d9a622 still governs; the tamper is reported only as a mirror mismatch."""
    root = tmp_path / "pin"
    subprocess.run(["git", "clone", "-q", "--shared", PIN, str(root)], check=True)
    subprocess.run(["git", "-C", str(root), "checkout", "-q", "4d9a622"], check=True)
    lock = root / "cycle3" / "requirements.lock.txt"
    lock.write_bytes(lock.read_bytes().replace(b"numpy==2.4.4", b"numpy==9.9.9"))
    pins, digest, mirror = read_lock_pins(str(root))
    assert pins["numpy"] == "2.4.4" and digest == EXPECTED_LOCK_SHA256 and mirror is False
    assert check_environment(str(root)).lock_worktree_mirror_matches is False

@needs_pin
def test_tampered_blob_digest_refuses_before_comparison(monkeypatch):
    from mfa_instrument.gates.gate_b import environment as E
    monkeypatch.setattr(E, "EXPECTED_LOCK_SHA256", "0" * 64)
    with pytest.raises(EnvironmentCheckError, match="digest FAILED"):
        read_lock_pins(PIN)

def test_environment_git_failure_is_named(tmp_path):
    with pytest.raises(EnvironmentCheckError, match="unreadable|unavailable"):
        read_lock_pins(str(tmp_path))

@needs_pin
def test_environment_decode_and_parse_failures_are_named(monkeypatch):
    from mfa_instrument.gates.gate_b import environment as E
    import subprocess as sp
    class R:  # fake completed process
        def __init__(self, out): self.returncode = 0; self.stdout = out; self.stderr = b""
    for payload, msg in ((b"\xff\xfe\x00bad", "digest FAILED"),):
        monkeypatch.setattr(E.subprocess, "run", lambda *a, **k: R(payload))
        with pytest.raises(EnvironmentCheckError, match=msg):
            read_lock_pins(PIN)
    good = open(os.path.join(PIN, "cycle3", "requirements.lock.txt"), "rb").read()
    dup = good + b"numpy==2.4.4\n"
    monkeypatch.setattr(E.subprocess, "run", lambda *a, **k: R(dup))
    monkeypatch.setattr(E, "EXPECTED_LOCK_SHA256", __import__("hashlib").sha256(dup).hexdigest())
    with pytest.raises(EnvironmentCheckError, match="duplicate pin"):
        read_lock_pins(PIN)

@needs_pin
def test_reference_blob_read_failure_is_reference_error_and_mirror_unreadability_is_provenance(monkeypatch):
    """git-show failure (nonzero) and git unavailability (OSError) are ReferenceErrors; an unreadable
    MIRROR is recorded as provenance (readable False, no digest, no match) and does not fail identity."""
    import subprocess as sp
    real_run = sp.run
    def failing_show(cmd, *a, **k):
        if cmd[:2] == ["git", "-C"] and "show" in cmd:
            class Rr: returncode = 128; stdout = b""; stderr = b"fatal: simulated"
            return Rr()
        return real_run(cmd, *a, **k)
    monkeypatch.setattr(sp, "run", failing_show)
    with pytest.raises(R.ReferenceError, match="blob 4d9a622:cycle3/wave_two/c3_w2_tcop.py unreadable"):
        R.load_pinned_reference(PIN)
    monkeypatch.undo()
    monkeypatch.setattr(sp, "run", lambda cmd, *a, **k: (_ for _ in ()).throw(OSError("no git")) if "show" in cmd else real_run(cmd, *a, **k))
    with pytest.raises(R.ReferenceError, match="git unavailable"):
        R.load_pinned_reference(PIN)
    monkeypatch.undo()
    real_open = open
    def bad_open(path, *a, **k):
        if str(path).endswith("c3_w2_tcop.py") and a and "rb" in a:
            raise PermissionError("simulated")
        return real_open(path, *a, **k)
    monkeypatch.setattr("builtins.open", bad_open)
    r = R.load_pinned_reference(PIN); pv = r.provenance
    assert pv.observed_sha256 == R.EXPECTED_SHA256 and pv.worktree_mirror_readable is False
    assert pv.worktree_mirror_sha256 is None and pv.worktree_mirror_matches_blob is None


@needs_pin
def test_environment_true_post_digest_invalid_utf8_is_named(monkeypatch):
    """Invalid UTF-8 bytes bound to the frozen digest: identity passes, decoding fails, named."""
    from mfa_instrument.gates.gate_b import environment as E
    bad = b"\xef\xbb\xbfnumpy==2.4.4\n\xff\xfe\x00broken\n"
    class R:
        returncode = 0; stdout = bad; stderr = b""
    monkeypatch.setattr(E.subprocess, "run", lambda *a, **k: R())
    monkeypatch.setattr(E, "EXPECTED_LOCK_SHA256", __import__("hashlib").sha256(bad).hexdigest())
    with pytest.raises(EnvironmentCheckError, match="not UTF-8"):
        read_lock_pins(PIN)
