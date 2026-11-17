from pathlib import Path
import json
import shutil
import sys
import tempfile

packet = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(packet / 'flights/mfa_fidelity/instrument'))
from mfa_instrument.f9 import config as C
from mfa_instrument.f9 import identities as I


def check(directory, relative_tolerance):
    try:
        I.verify_bundle_deep(str(directory), float_rtol=relative_tolerance)
        return {'outcome': 'ACCEPTED', 'error': None}
    except C.F9ConfigError as exc:
        return {'outcome': 'REJECTED', 'error': str(exc)}


results = []
with tempfile.TemporaryDirectory(prefix='l2_f9_m1_round2_') as scratch:
    scratch = Path(scratch)
    control = scratch / 'control'
    I.write_bundle(str(control))
    assert check(control, 0.0)['outcome'] == 'ACCEPTED'
    print('UNCHANGED CONTROL: ACCEPTED', flush=True)
    for label, nudge, coherent_gain in (
        ('spectral_only', 1.004e-9, False),
        ('coherent_pair', 1.0003e-9, True),
    ):
        changed = scratch / label
        shutil.copytree(control, changed)
        path = changed / I.RECORD_NAME
        record = json.loads(path.read_bytes())
        reference = record['arms']['TB.P']['spr']
        stated = reference * (1.0 + nudge)
        record['arms']['TB.P']['spr'] = stated
        if coherent_gain:
            record['arms']['TB.P']['g_spec'] = record['q'] / (C.F9_DT * stated)
        path.write_bytes(I.canonical_json(record))
        difference = abs(stated - reference)
        relative = difference / abs(stated)
        assert relative > C.F9_SPR_RECOMPUTE_RTOL
        item = {
            'case': label,
            'recomputed_spr': reference,
            'stated_spr': stated,
            'absolute_difference': difference,
            'relative_to_stated': relative,
            'relative_to_recomputed': difference / abs(reference),
            'frozen_relative_allowance': C.F9_SPR_RECOMPUTE_RTOL * abs(stated),
            'current_mixed_allowance': (
                C.F9_SPR_RECOMPUTE_RTOL * max(abs(stated), abs(reference))
                + C.F9_CROSS_PLATFORM_TOL
            ),
            'exact': check(changed, 0.0),
            'cross_machine': check(changed, C.F9_SPR_RECOMPUTE_RTOL),
        }
        results.append(item)
        print(json.dumps(item, sort_keys=True), flush=True)

if len(sys.argv) > 2:
    Path(sys.argv[2]).write_text(json.dumps(results, indent=2) + '\n')
