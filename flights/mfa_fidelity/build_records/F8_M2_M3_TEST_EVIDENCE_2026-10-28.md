# Flight 8 M2/M3 — test evidence of record, canonical machine, 2026-10-28

Captured outputs transcribed verbatim from Mike's canonical machine (CHA-88D57D3, Windows-11-10.0.26200-SP0; Python 3.14.4, numpy 2.4.4, pyarrow 24.0.0, pandas 3.0.3, pytest 9.0.3 — the twenty-pin canonical venv; `MFA_PINNED_REPO_ROOT = C:\Users\vkz244\EE_Theory_Lab\pinned-4d9a622` for the suite run). Working tree: HEAD `0f30400d982ff6ec4901084ca5f4c43822518eda` plus the staged M2/M3 files at the identities named in the round-3 response (`null.py` 4ee3f239b27f772b…, `test_f8_m2_m3.py` d0d26e75280dffef…, `classify.py` 42daeb4663c5783f…, `dynamics.py` cc663dd3c14197a8…, `test_f8_m1.py` 23d4260f5a2d996b…). The output files remain on that machine in Downloads; their SHA-256 digests are stated so the transcription can be checked against them.

## 1. M2/M3 module alone, whole module, one process (L2 V1)

Command (from `flights/mfa_fidelity/instrument`): `python -m pytest tests\test_f8_m2_m3.py -q -p no:cacheprovider` — exit code **0**; output file `f8_m2_m3_module_2026-10-28.txt`, SHA-256 `92756dfaf3564367b85ebb917783f75b8c10c178bf3481406e178faf6a82c83f`:

```
..................................                                       [100%]
34 passed in 65.18s (0:01:05)
```

## 2. Canonical suite, whole, pinned root set (L2 H2)

Command: `python -m pytest tests -q -p no:cacheprovider` — output file `f8_m2_m3_suite_2026-10-28.txt`, SHA-256 `8603cbaf338588e0477656b54f3b1a15c1e7b95b4f84409227fc54bd380e8f8b`:

```
........................................................................ [ 10%]
........................................................................ [ 21%]
................................................................s....... [ 31%]
........................................................................ [ 42%]
........................................................................ [ 52%]
........................................................................ [ 63%]
........................................................................ [ 74%]
........................................................................ [ 84%]
.....s.................................................................. [ 95%]
................................                                         [100%]
678 passed, 2 skipped in 3032.67s (0:50:32)
```

678 = 575 (suite of record at M7 placement) + 69 (`test_f8_m1.py`) + 34 (`test_f8_m2_m3.py`); the 2 skips are the two declared skips of record.

*Transcribed by L1 from Mike's pasted clipboard, 2026-10-28.*
