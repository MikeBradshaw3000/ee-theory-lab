"""Synthetic domain witness for I002 draft1 Point8; no scientific data or job."""
import hashlib
import json
from pathlib import Path
import numpy as np

OUT = Path(__file__).resolve().parent
counts = np.zeros((40, 100, 100), dtype=np.int64)
counts[:19, 30:50, 30:50] = 400
observed_weights = np.ones(40, dtype=np.int64)
draw_weights = observed_weights.copy()
draw_weights[0] = 2  # one active-map occurrence repeated
# 19 active maps now have 20 occurrences; 21 zero maps have 20 occurrences.
draw_weights[19] = 0
assert int(draw_weights.sum()) == 40
assert np.all(draw_weights >= 0)
THRESHOLD_NUMERATOR = 40 * 1000 * 9 // 5  # theta=1/5, on integer box sums

def inspect(weights):
    weighted_counts = np.tensordot(weights, counts, axes=(0, 0))
    box_sum = sum(np.roll(np.roll(weighted_counts, dy, axis=0), dx, axis=1)
                  for dy in (-1, 0, 1) for dx in (-1, 0, 1))
    region = box_sum >= THRESHOLD_NUMERATOR
    neighbors = [np.roll(region, k, axis=ax) for ax in (0,1) for k in (-1,1)]
    inside = region & np.logical_or.reduce([~m for m in neighbors])
    outside = ~region & np.logical_or.reduce(neighbors)
    bonds = sum(int(np.count_nonzero(region != np.roll(region, 1, axis=ax)))
                for ax in (0,1))
    return {
        'active_map_occurrences': int(weights[:19].sum()),
        'zero_map_occurrences': int(weights[19:].sum()),
        'maximum_unsmoothed_mean': int(weighted_counts.max()) / 40000,
        'maximum_box_numerator': int(box_sum.max()),
        'threshold_numerator': THRESHOLD_NUMERATOR,
        'region_cells': int(region.sum()),
        'complement_cells': int((~region).sum()),
        'boundary_bonds': bonds,
        'distinct_inside_edge_cells': int(inside.sum()),
        'distinct_outside_edge_cells': int(outside.sum()),
        'step4_informative': bool(region.sum() >= 100 and (~region).sum() >= 100 and bonds >= 40),
    }

point = inspect(observed_weights)
draw = inspect(draw_weights)
assert point['maximum_box_numerator'] == 68400
assert point['region_cells'] == point['boundary_bonds'] == 0
assert draw['maximum_box_numerator'] == 72000
assert (draw['region_cells'],draw['boundary_bonds']) == (324,72)
assert (draw['distinct_inside_edge_cells'],draw['distinct_outside_edge_cells']) == (68,72)
assert draw['step4_informative']
result = {
    'purpose': 'Positive-support synthetic witness that a draw can define edge-cell statistics while the observed map cannot.',
    'data_origin': 'Constructed integer arrays only; no scientific job, probe array, master draw, or source modification.',
    'maps': '40 maps on 100x100; first19 have400/1000 occupancy on a20x20 patch; other21 are zero.',
    'point': point,
    'valid_draw': draw,
    'draw_weights': draw_weights.tolist(),
    'closure_dependency_for_case': 'Nonconverged/unavailable by hypothesis; no closure solver run.',
    'case': 'Point2/3 edge-cell summaries absent at point; Point5/6/7 closure-dependent summaries absent by hypothesis. Yet Point2 and the minus1 contrast in Point3 are numerically defined on the valid draw. A draw trigger requiring any observed summary can omit conditional ranges.',
    'limits': 'One possible replacement draw, not a claim about which draws a canonical stream produces; no proposed extension of scored step9 applicability.',
    'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
}
(OUT/'draw_gate_witness.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
