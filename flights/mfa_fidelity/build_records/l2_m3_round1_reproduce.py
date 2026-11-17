import numpy as np
from mfa_instrument.f9.evaluator import check_weights

w = np.zeros(40, dtype=np.uint64)
w[0] = np.uint64(2**64 - 1)
w[1] = np.uint64(41)
assert int(w.sum()) == 40  # wrapped, not the mathematical sum
accepted = check_weights(w)  # MUST raise; currently returns
assert accepted[0] == -1 and accepted[1] == 41
print('DEFECT REPRODUCED: invalid multiplicities accepted:', accepted[:2])
