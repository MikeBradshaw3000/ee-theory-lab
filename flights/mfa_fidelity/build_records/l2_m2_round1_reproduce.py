"""L2 F9 M2 round-1 witnesses. Pass the extracted packet root as argv[1].

Uses only test master 7 for dynamics. Historical masters are checked as
integers only: no generator or trajectory is created under them.
"""
from pathlib import Path
import ast
import copy
from dataclasses import replace
import hashlib
import json
import struct
import sys
import tempfile

import numpy as np

packet = Path(sys.argv[1]).resolve()
instrument = packet / "flights/mfa_fidelity/instrument"
sys.path.insert(0, str(instrument))
from mfa_instrument.f9 import config as C, dynamics as D, identities as I, streams as R

expected = {
    "mfa_instrument/f9/streams.py": "1d1bbc48abe1df54fed25c072402d64ced71a2b3b85a44cf818fb783b90afaec",
    "mfa_instrument/f9/dynamics.py": "11ad2ef15ef30520018ee15501cd43d5f7bd126c4e268e398c85ed7ad9cafed3",
    "mfa_instrument/f8/audit.py": "81feaab6eb766c101f015663e99a3177c74d1a7ea00a28c572bc38428f38373e",
}
for rel, digest in expected.items():
    assert hashlib.sha256((instrument / rel).read_bytes()).hexdigest() == digest, rel


def emit(case, **facts):
    print(json.dumps({"case": case, **facts}, sort_keys=True), flush=True)


# R2: obtain the historical retired values independently of the F9 list.
tree = ast.parse((instrument / "mfa_instrument/f8/audit.py").read_text())
retired = next(
    ast.literal_eval(node.value)
    for node in tree.body
    if isinstance(node, ast.Assign)
    and any(isinstance(t, ast.Name) and t.id == "E1_RETIRED_MASTERS" for t in node.targets)
)
for master in retired:
    assert master not in R.RETIRED_MASTERS
    assert R.check_master(master) == master
    assert R.master_class(master) == "stage"
    emit("R2_retired_master_accepted", master=master, classification=R.master_class(master))

# This is a local test bundle, not the canonical machine's identity bundle.
with tempfile.TemporaryDirectory(prefix="l2_f9_m2_") as temp:
    I.write_bundle(temp)
    record, arrays = I.load_bundle(temp)
    arm = D.arm_context(record, arrays, "T0", "P")

spec = D.F9RunSpec(7, "T0", "P", "realization", "stationary_floor", 1500000, 0)
result = D.run(spec, arm)
original = D.serialize_run(result)
assert D.replay_equals(original, arm)
emit("unaltered_control", parse="ACCEPTED", replay=True)


def copy_windows():
    return {W: {k: v.copy() for k, v in row.items()} for W, row in result.windows.items()}


def check_blob(case, blob, **facts):
    # Parsing checks every stated hash. Serialization below recomputes them.
    D.parse_run(blob)
    replay = D.replay_equals(blob, arm)
    assert replay is False
    emit(case, parse="ACCEPTED", replay=replay, **facts)


# R1a: W=1 endpoints are exactly the states at ticks 2001 and 3000.
for endpoint, tick in (("first", C.F9_TICKS - C.F9_TAIL_TICKS + 1),
                       ("last", C.F9_TICKS)):
    windows = copy_windows()
    eligible = windows[1][endpoint] & (windows[1]["R0"] >= 2) & (windows[1]["A"] >= 3)
    cells = np.argwhere(eligible)
    assert len(cells), "No endpoint witness on this environment"
    cell = tuple(int(v) for v in cells[0])
    windows[1][endpoint][cell] = False
    endpoint_total = int(windows[1][endpoint].sum())
    count = int(result.counts[tick])
    assert endpoint_total != count
    bad = D.serialize_run(replace(result, windows=windows))
    check_blob("R1a_" + endpoint + "_endpoint", bad,
               cell=cell, endpoint_total=endpoint_total, tick=tick, count=count)

# R1b: an active 100-tick window contains at most ten active 10-tick windows.
windows = copy_windows()
lower = (windows[1]["A"] + 99) // 100
eligible = (windows[10]["A"] > 10 * lower) & (lower >= 2) & (lower < 10)
cells = np.argwhere(eligible)
assert len(cells), "No nested-window witness on this environment"
cell = tuple(int(v) for v in cells[0])
windows[100]["A"][cell] = lower[cell]
windows[100]["R0"][cell] = 1
A1, A10, A100 = (int(windows[W]["A"][cell]) for W in (1, 10, 100))
assert A10 > 10 * A100
bad = D.serialize_run(replace(result, windows=windows))
check_blob("R1b_nested_windows", bad, cell=cell, A_W1=A1, A_W10=A10,
           A_W100=A100, maximum_W10_given_W100=10 * A100)

# R1c: equality of numeric values is not validation of integer JSON types.
hlen = struct.unpack("<I", original[8:12])[0]
header = json.loads(original[12:12 + hlen])
body = original[12 + hlen:]
for case, field, value in (
    ("R1c_float_stream_key", "stream_key", [float(v) for v in spec.stream_key]),
    ("R1c_bool_window", "windows", [True, 10, 100]),
):
    changed = copy.deepcopy(header)
    changed[field] = value
    raw = I.canonical_json(changed)
    bad = D.RUN_MAGIC + struct.pack("<I", len(raw)) + raw + body
    check_blob(case, bad, field=field, value=value)

emit("witnesses_complete", retired_identities=3, malformed_records=5,
     all_malformed_records_rejected_by_replay=True)
