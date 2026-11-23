"""f9_m6_mutation_check.py — L1's mutation check of tests/test_f9_m6.py against mfa_instrument/f9/reports.py.

Usage: python f9_m6_mutation_check.py <path to a COPY of flights/mfa_fidelity/instrument>
Round 2 (2026-11-23): the between-width and floor-reference mutations are added.
Each mutation replaces one source fragment in the copy's reports.py, runs the M6 test file, and restores the source.
CAUGHT = at least one test failed. The copy is left with the original bytes. Nothing here is part of the instrument."""
import hashlib, os, subprocess, sys

root = os.path.abspath(sys.argv[1])
path = os.path.join(root, "mfa_instrument", "f9", "reports.py")
src = open(path, encoding="utf-8").read()
MUTATIONS = [
    ("cut tie excluded", "values * C.MICRO_UNITS >= micro", "values * C.MICRO_UNITS > micro"),
    ("bin closes above 100", "if size >= BIN_MIN_CELLS:", "if size > BIN_MIN_CELLS:"),
    ("short final bin kept", "if len(edges) > 1: edges[-1] = flat.size", "if len(edges) > 1: edges.append(flat.size)"),
    ("noise divisor 40*40", "(D_ * D_ * n * (n - 1) * N)", "(D_ * D_ * n * n * N)"),
    ("noise on X_s, not the residual", "noise += _within_bin_sum_of_squares(n * c[s] - t,", "noise += _within_bin_sum_of_squares(n * c[s],"),
    ("censored needs both ends", "int((~first | ~last).sum())", "int((~first & ~last).sum())"),
    ("censored counted among defined only (EQUIVALENT: an undefined record is all-active)", "int((~first | ~last).sum())", "int(((~first | ~last) & defined).sum())"),
    ("quartile weight r/3", "* (r / 4))", "* (r / 3))"),
    ("statistic without W", "np.sort((W * (n - A[defined])) / R0[defined])", "np.sort((n - A[defined]) / R0[defined])"),
    ("statistic over R0 + 1", "np.sort((W * (n - A[defined])) / R0[defined])", "np.sort((W * (n - A[defined])) / (R0[defined] + 1))"),
    ("band edges one micro-unit up", "band += _at_least(t, edge, OCC_DENOMINATOR)", "band += _at_least(t, edge + 1, OCC_DENOMINATOR)"),
    ("0.20 band uses the 0.30 cut", "pair(ge20, ge10 & ~ge20)", "pair(ge20, ge10 & ~ge30)"),
    ("outside set is everything not inside", "bump <= TC_OUTSIDE_BUMP_MAX", "bump < TC_INSIDE_BUMP_MIN"),
    ("ratio inverted", "m_in / m_out", "m_out / m_in"),
    ("bins ordered by descending omega", 'order = np.argsort(flat, kind="stable")', 'order = np.argsort(-flat, kind="stable")'),
    ("margins on the unsmoothed map", "B = E.box_sum(t)", "B = 9 * t"),
    ("record check dropped: R0 = 0 iff A = n", "or bool(((R0 == 0) != (A == n)).any())", ""),
    ("record check dropped: Ra <= A", "or bool((Ra > A).any())", ""),
    ("record check dropped: Ra >= 0", "or bool((Ra < 0).any())", ""),
    ("record check dropped: R0 <= n - A", "bool((R0 > n - A).any()) or", ""),
    ("record check dropped: Ra = 0 iff A = 0", "or bool(((Ra == 0) != (A == 0)).any())", ""),
    ("TC set sizes not asserted", "if (int(inside.sum()), int(outside.sum())) != TC_SET_SIZES:", "if False:"),
    ("nesting dropped: A_l <= A_s", 'bool((l["A"] > s["A"]).any()) or', ""),
    ("nesting dropped: A_s <= k A_l", 'or bool((s["A"] > k * l["A"]).any())', ""),
    ("nesting dropped: R0_l <= R0_s (EQUIVALENT: implied by the Ra relation and the two end implications; L2 round 1, D1)", 'bool((l["R0"] > s["R0"]).any()) or', ""),
    ("nesting dropped: Ra_l <= Ra_s", 'or bool((l["Ra"] > s["Ra"]).any())', ""),
    ("nesting dropped: first_s implies first_l", 'bool((s["first"] & ~l["first"]).any()) or', ""),
    ("nesting dropped: last_s implies last_l", 'or bool((s["last"] & ~l["last"]).any())', ""),
    ("nesting skips the pair (1, 100) (EQUIVALENT: implied by the pairs (1, 10) and (10, 100), every relation being transitive)", "if Wl <= Ws or Wl % Ws: continue", "if Wl <= Ws or Wl % Ws or Wl == 100 * Ws: continue"),
    ("floor reference exponent W", "(1.0 - a) ** (W - 1)", "(1.0 - a) ** W"),
    ("floor literals for W = 10 and 100 exchanged", '(10, "0.1342"), (100, "0.6496"))', '(10, "0.6496"), (100, "0.1342"))'),
    ("flicker record without its floor reference", '"bands": out_bands, "floor_reference": floor,', '"bands": out_bands,'),
    ("V_within without bin centring", "v_within = _within_bin_sum_of_squares(t, order, starts, sizes) / (D_ * D_ * N)", "v_within = Fraction(int((t * t).sum())) / (D_ * D_ * N)"),
]
print("reports.py", hashlib.sha256(src.encode("utf-8")).hexdigest())
caught = 0
try:
    for name, a, b in MUTATIONS:
        assert src.count(a) == 1, name
        open(path, "w", encoding="utf-8", newline="\n").write(src.replace(a, b))
        r = subprocess.run([sys.executable, "-B", "-m", "pytest", "tests/test_f9_m6.py", "-q", "-x", "-p", "no:cacheprovider"], cwd=root, capture_output=True, text=True)
        caught += bool(r.returncode)
        print(("CAUGHT  " if r.returncode else "MISSED  ") + name)
finally:
    open(path, "w", encoding="utf-8", newline="\n").write(src)
print(f"{caught} of {len(MUTATIONS)} caught")
print("reports.py restored", hashlib.sha256(open(path, "rb").read()).hexdigest())
