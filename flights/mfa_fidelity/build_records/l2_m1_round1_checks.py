from pathlib import Path
import copy
import hashlib
import json
import shutil
import sys
import tempfile

import numpy as np

packet = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(packet / "flights/mfa_fidelity/instrument"))
from mfa_instrument.f9 import config as C
from mfa_instrument.f9 import family as F
from mfa_instrument.f9 import geometry as G
from mfa_instrument.f9 import identities as I


def outcome(call):
    try:
        call()
        return "ACCEPTED"
    except C.F9ConfigError:
        return "REJECTED"


# R1: fixed omega, fixed canonical bond points, different component membership.
x, y = np.indices((100, 100))
omega = ((x // 10 + y // 10) % 2).astype(np.float64)
mask = omega >= 1
correct = G.edge(mask)
other = G.edge(~mask)
assert np.array_equal(correct.points, other.points)
assert correct.component_sizes() == other.component_sizes() == (40,) * 50
assert not np.array_equal(correct.component, other.component)
a = F.family_summary(omega)
original_edge = G.edge
try:
    G.edge = lambda m: original_edge(~m)
    b = F.family_summary(omega)
finally:
    G.edge = original_edge
print("R1", json.dumps({
    "bonds": correct.n_bonds,
    "components": correct.n_components,
    "different_labels": int(np.count_nonzero(correct.component != other.component)),
    "summaries_equal": a == b,
    "component_hashes_equal": a["components_sha256"] == b["components_sha256"],
}))

# R1 endian witness; the review host is little endian.
print("byteorder", sys.byteorder)
print("scalar_requested_big_endian",
      np.float64(1.25).astype(">f8").tobytes().hex())
print("array_requested_big_endian",
      np.asarray([1.25], dtype=">f8").tobytes().hex())

# R3: in-memory altered source, unchanged bound rule; original files untouched.
source = Path(C.__file__).read_text()
old = "F9_ETA0 = -math.log(1.0 - 0.01)"
new = "F9_ETA0 = -math.log(1.0 - 0.02)"
assert source.count(old) == 1
scope = {
    "__name__": "mfa_instrument.f9._l2_eta_probe",
    "__package__": "mfa_instrument.f9",
}
exec(compile(source.replace(old, new), "<L2 in-memory eta0 probe>", "exec"), scope)
try:
    checked = scope["verify_frozen_identity"]()
    eta_result = {
        "outcome": "ACCEPTED",
        "eta0": scope["F9_ETA0"],
        "declaration_unchanged":
            checked["declaration_sha256"] == C.F9_DECLARATION_SHA256_LITERAL,
    }
except scope["F9ConfigError"]:
    eta_result = {"outcome": "REJECTED"}
print("R3", json.dumps(eta_result))


def empty_coverage(r, directory):
    r["arms"] = {}
    r["families"] = {}
    r["same_family"] = {}


def wrong_gain(r, directory):
    r["arms"]["TB.H"]["g_spec"] *= 2.0


def wrong_comparison(r, directory):
    raw = (directory / "omega/TB.P.f64").read_bytes()
    (directory / "omega/TB.H.f64").write_bytes(raw)
    r["arrays"]["omega/TB.H.f64"] = hashlib.sha256(raw).hexdigest()
    r["families"]["TB.H"] = copy.deepcopy(r["families"]["TB.P"])


def wrong_arm_binding(r, directory):
    r["arms"]["TC.H"]["omega_key"] = "TB.P"


with tempfile.TemporaryDirectory(prefix="l2_f9_m1_review_") as work:
    work = Path(work)
    control = work / "control"
    I.write_bundle(str(control))
    I.verify_bundle_deep(str(control))
    print("R2 unchanged control: ACCEPTED")
    for name, mutate in (
        ("empty_coverage", empty_coverage),
        ("wrong_gain", wrong_gain),
        ("wrong_comparison", wrong_comparison),
        ("wrong_arm_binding", wrong_arm_binding),
    ):
        directory = work / name
        shutil.copytree(control, directory)
        record = json.loads((directory / I.RECORD_NAME).read_bytes())
        mutate(record, directory)
        (directory / I.RECORD_NAME).write_bytes(I.canonical_json(record))
        print("R2", name, outcome(lambda: I.verify_bundle_deep(str(directory))))
