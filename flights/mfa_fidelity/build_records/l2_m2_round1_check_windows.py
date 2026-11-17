"""Independent exhaustive checks of the observed-inactive-segment definition; no run or master."""
from pathlib import Path
import sys
import itertools
import json
import numpy as np

packet = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(packet / 'flights/mfa_fidelity/instrument'))
from mfa_instrument.f9.dynamics import _Windows

report=[]
for W, nwin in [(1,12),(10,12),(100,10)]:
    ncell=2**nwin
    L=int(np.sqrt(ncell))
    assert L*L == ncell
    sequences=[list(bits) for bits in itertools.product((False,True),repeat=nwin)]
    active=np.array(sequences,dtype=bool).T.reshape(nwin,L,L)
    expected_A=np.array([sum(s) for s in sequences]).reshape(L,L)
    expected_R0=np.array([sum(1 for bit,_ in itertools.groupby(s) if not bit) for s in sequences]).reshape(L,L)
    offsets=np.arange(ncell).reshape(L,L) % W
    acc=_Windows(W,L)
    for j in range(nwin):
        for t in range(W):
            acc.add(active[j] & (offsets == t))
    assert acc.n==nwin and acc._k==0
    assert np.array_equal(acc.A,expected_A)
    assert np.array_equal(acc.R0,expected_R0)
    assert np.array_equal(acc.first,active[0])
    assert np.array_equal(acc.last,active[-1])
    report.append({'W':W,'window_count':nwin,'exhaustive_binary_window_histories':ncell,'checks':['A','R0 by maximal zero runs','first','last','window count'],'passed':True})
print(json.dumps({'scope':'deterministic window accumulation only; no dynamics, no run, no master', 'results':report},indent=2))
