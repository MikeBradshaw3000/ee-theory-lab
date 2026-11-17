"""L2's M2 round-1 Appendix A witnesses, adapted by L1 to REPORT outcomes instead of asserting acceptance.

Changes from L2's program (l2_m2_round1_reproduce.py): the source-hash guards are removed so that it runs on any
round's bytes; each `assert ... accepted` is replaced by a printed outcome. The witness constructions are L2's, unchanged.
Pass the root that contains flights/mfa_fidelity/instrument as argv[1]. Test master 7 only; historical masters are
checked as integers, and no generator is created under them.
"""
from pathlib import Path
import ast
import copy
from dataclasses import replace
import json
import struct
import sys
import tempfile

import numpy as np

packet = Path(sys.argv[1]).resolve()
instrument = packet / "flights/mfa_fidelity/instrument"
sys.path.insert(0, str(instrument))
from mfa_instrument.f9 import config as C, dynamics as D, identities as I, streams as R


def emit(case, **facts):
    print(json.dumps({"case": case, **facts}, sort_keys=True), flush=True)


def outcome(fn, *a):
    try: fn(*a)
    except (C.F9ConfigError, D.F9DynamicsError) as e: return "REFUSED: " + str(e)[:90]
    return "ACCEPTED"


tree = ast.parse((instrument / "mfa_instrument/f8/audit.py").read_text())
retired = next(
    ast.literal_eval(node.value)
    for node in tree.body
    if isinstance(node, ast.Assign)
    and any(isinstance(t, ast.Name) and t.id == "E1_RETIRED_MASTERS" for t in node.targets)
)
for master in retired:
    emit("R2_retired_master", master=master, check_master=outcome(R.check_master, master))

with tempfile.TemporaryDirectory(prefix="l1_f9_m2_") as temp:
    I.write_bundle(temp)
    record, arrays = I.load_bundle(temp)
    arm = D.arm_context(record, arrays, "T0", "P")

spec = D.F9RunSpec(7, "T0", "P", "realization", "stationary_floor", 1500000, 0)
result = D.run(spec, arm)
original = D.serialize_run(result)
emit("unaltered_control", parse=outcome(D.parse_run, original), replay=D.replay_equals(original, arm))


def copy_windows():
    return {W: {k: v.copy() for k, v in row.items()} for W, row in result.windows.items()}


for endpoint, tick in (("first", C.F9_TICKS - C.F9_TAIL_TICKS + 1), ("last", C.F9_TICKS)):
    windows = copy_windows()
    eligible = windows[1][endpoint] & (windows[1]["R0"] >= 2) & (windows[1]["A"] >= 3)
    cell = tuple(int(v) for v in np.argwhere(eligible)[0])
    windows[1][endpoint][cell] = False
    bad = D.serialize_run(replace(result, windows=windows))
    emit("R1a_" + endpoint + "_endpoint", parse=outcome(D.parse_run, bad), cell=cell,
         endpoint_total=int(windows[1][endpoint].sum()), tick=tick, count=int(result.counts[tick]))

windows = copy_windows()
lower = (windows[1]["A"] + 99) // 100
eligible = (windows[10]["A"] > 10 * lower) & (lower >= 2) & (lower < 10)
cell = tuple(int(v) for v in np.argwhere(eligible)[0])
windows[100]["A"][cell] = lower[cell]
windows[100]["R0"][cell] = 1
bad = D.serialize_run(replace(result, windows=windows))
emit("R1b_nested_windows", parse=outcome(D.parse_run, bad), cell=cell,
     A_W1=int(windows[1]["A"][cell]), A_W10=int(windows[10]["A"][cell]), A_W100=int(windows[100]["A"][cell]))

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
    emit(case, parse=outcome(D.parse_run, bad), field=field)
