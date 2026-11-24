"""f9_m6b_mutation_check.py — L1's mutation check of tests/test_f9_m6b.py against mfa_instrument/f9/evaluator_reports.py.

Usage: python f9_m6b_mutation_check.py <path to a COPY of flights/mfa_fidelity/instrument>
Each mutation replaces one source fragment in the copy, runs the tests named for it (pytest -k; the evaluator tests take
minutes, so a mutation is run against the tests that bear on it and not against the whole file), and restores the source.
CAUGHT = at least one of those tests failed. Nothing here is part of the instrument."""
import hashlib, os, subprocess, sys

root = os.path.abspath(sys.argv[1])
path = os.path.join(root, "mfa_instrument", "f9", "evaluator_reports.py")
src = open(path, encoding="utf-8").read()
CHEAP = "criterion or coverage or forty or design or persistence"
WRAP = "scored_threshold or reported_thresholds_against"
MUTATIONS = [
    ("theta ignored by the criterion", CHEAP, "_theta(theta_micro) * BOX_DENOMINATOR", "C.F9_THETA_MICRO * BOX_DENOMINATOR"),
    ("criterion tie excluded", CHEAP, "B * C.MICRO_UNITS >= _theta", "B * C.MICRO_UNITS > _theta"),
    ("any integer theta accepted", CHEAP, "type(theta_micro) is not int or theta_micro not in THETAS_ACCEPTED_MICRO", "type(theta_micro) is not int"),
    ("resamples from another stream", WRAP, "mult = E.resample_multiplicities(key)", "mult = E.resample_multiplicities(key + (0,))"),
    ("draws evaluated at the scored theta", WRAP, "draw = evaluate_map_at(counts, mult[r], applicable, theta_micro, brute)", "draw = evaluate_map_at(counts, mult[r], applicable, C.F9_THETA_MICRO, brute)"),
    ("point evaluated at the scored theta", WRAP, "point = evaluate_map_at(counts, ones, families, theta_micro, brute)", "point = evaluate_map_at(counts, ones, families, C.F9_THETA_MICRO, brute)"),
    ("the two reported thresholds exchanged", WRAP, "{t: evaluate_level_at(counts, families, key, t) for t in THETAS_REPORTED_MICRO}", "{t: evaluate_level_at(counts, families, key, 400_000 - t) for t in THETAS_REPORTED_MICRO}"),
    ("fitted label dropped", WRAP, 'if entry.get("within"): entry["lambda_star"] = fam.label(entry["level_index"])', "pass"),
    ("label range dropped", WRAP, 'entry["lambda_star_range"] = [min(labels), max(labels)]', 'entry["lambda_star_range"] = None'),
    ("unavailable cause not told apart", "two_families or outranks", 'point["reason"].startswith("no edge")', 'point["reason"].startswith("zzz")'),
    ("constant index takes the map's cause (the round-1 order)", "outranks", "if len(fam) == 0:   ", 'if len(fam) == 0 and point["informative"]:   '),
    ("a map with no edge labelled as a constant index", "outranks", "cause = E.CAUSE_NO_EDGE if point", "cause = E.CAUSE_NO_CONTOUR if len(fam) == 0 or point"),
    ("skeleton key without its object code", "skeleton", "level_micro, SKELETON_OBJECT_CODE)", "level_micro)"),
    ("skeleton boundary accepts any key", "skeleton", "if len(key) != 5 or key[-1] != SKELETON_OBJECT_CODE: raise", "if False: raise"),
    ("skeleton boundary at theta 0.10", "skeleton", '"evaluation": E.evaluate_level(counts, families, key),', '"evaluation": evaluate_level_at(counts, families, key, 100_000),'),
    ("resolved needs more than 40 bonds", CHEAP, '"resolved": bool(n >= C.F9_COMPONENT_MIN_BONDS)', '"resolved": bool(n > C.F9_COMPONENT_MIN_BONDS)'),
    ("observed resolved count needs more than 40", CHEAP, '"resolved": sum(1 for n in sizes if n >= C.F9_COMPONENT_MIN_BONDS)', '"resolved": sum(1 for n in sizes if n > C.F9_COMPONENT_MIN_BONDS)'),
    ("both sides measured from the observed edge", CHEAP, "obs, con = _side_components(Et, Cn), _side_components(Cn, Et)", "obs, con = _side_components(Et, Cn), _side_components(Cn, Cn)"),
    ("coverage against the neighbouring contour", CHEAP, 'Cn = fam.contour(f["level_index"])', 'Cn = fam.contour(max(0, f["level_index"] - 1))'),
    ("coverage distances to a component, not the whole edge", CHEAP, "d = E._cells(other.grid[mine.a, mine.b])", "d = E._cells(mine.grid[mine.a, mine.b])"),
    ("design table not asserted", CHEAP, '!= (perimeter, band_cells, ratio_lit, step_lit):', '!= (perimeter, band_cells, ratio_lit, step_lit) and False:'),
    ("design core not checked against the base", CHEAP, "if not np.array_equal(core, a > TD_BASE_LOW + TD_BASE_STEP / 2): raise", "if False: raise"),
    ("design band inclusive (EQUIVALENT on these terrains: no cell within 1e-4 of either limit)", CHEAP, "band = (S > TD_BAND[0]) & (S < TD_BAND[1])", "band = (S >= TD_BAND[0]) & (S <= TD_BAND[1])"),
    ("design band split exchanged", CHEAP, '"inside_core": int((band & core).sum()), "outside_core": int((band & ~core).sum())', '"inside_core": int((band & ~core).sum()), "outside_core": int((band & core).sum())'),
    ("persistence complete despite missing levels", CHEAP, '"complete": not missing and not incomplete', '"complete": not missing'),
    ("missing arm not listed", CHEAP, "arms[n] = None; missing.append(n)", "arms[n] = None"),
    ("persistence accepts undeclared arms", CHEAP, "any(type(k) is not str or k not in names for k in survivors_by_arm)", "False"),
]
print("evaluator_reports.py", hashlib.sha256(src.encode("utf-8")).hexdigest())
caught = 0
try:
    for name, tests, a, b in MUTATIONS:
        assert src.count(a) == 1, name
        open(path, "w", encoding="utf-8", newline="\n").write(src.replace(a, b))
        r = subprocess.run([sys.executable, "-B", "-m", "pytest", "tests/test_f9_m6b.py", "-q", "-x", "-p", "no:cacheprovider", "-k", tests], cwd=root, capture_output=True, text=True)
        caught += bool(r.returncode)
        print(("CAUGHT  " if r.returncode else "MISSED  ") + name + "   [-k " + tests + "]"); sys.stdout.flush()
finally:
    open(path, "w", encoding="utf-8", newline="\n").write(src)
print(f"{caught} of {len(MUTATIONS)} caught")
print("evaluator_reports.py restored", hashlib.sha256(open(path, "rb").read()).hexdigest())
