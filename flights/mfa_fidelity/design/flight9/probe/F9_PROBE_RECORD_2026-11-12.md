# Flight 9 — pre-contract probe record (2026-11-12)
**Register.** NONCANONICAL design evidence only, under `FLIGHT_9_PRE_PROBE_DECLARATION_v1_0.md` (`473a2a165fd5cb4e…`, ratified by Mike 2026-11-12, committed at `0eef0f0`). Nothing here is a Flight 9 result, a calibration, a qualification or a canonical observation, and no Flight 9 result may be represented as independent of it. Every number below was written by script from `F9_PROBE_REPORT_2026-11-12.json`.
## 1. What ran
- The declared menu, once, to completion: **896 of 896 runs**, no error, no configuration added, repeated or dropped.
- Run by L1 in the Linux container from a fresh clone at `0eef0f07486172ff19d3e317829e999eeefd79e2`: script `f9_probe.py` `da5fd84b00818fcd…`, declaration `473a2a165fd5cb4e…` (both recorded by the run in its manifest). Platform `Linux-6.18.44-fc-v378-x86_64-with-glibc2.39`, Python 3.13.18, NumPy 2.5.3.
- Started 2026-11-12 20:08:07 UTC; complete by 20:17:20 UTC (observed). Sum of per-run wall time 9.0 min.
- 189 skeleton runs went extinct; each is a valid observation.
| Object | Bytes | SHA-256 |
|---|---|---|
| `F9_PROBE_MANIFEST_2026-11-12.json` (beside this file) | 450,019 | `b2e61476dceccd593f5faf7babd18108e4db68497cfbf721cd78d1e49d9130fc` |
| `F9_PROBE_REPORT_2026-11-12.json` (beside this file) | 144,810 | `59cfce5ffbd24512a1301da67748eda8a5ced8efec32efed5eebd8b464a51679` |
| `f9_probe_arrays_2026-11-12.zip` (896 array files and the manifest; delivered to Mike, **not in the repository**) | 23,221,854 | `516bedfabd96d063dd927171e8d44d5633774fdcb7280b1fdbf5dfc5a88f8005` |

All 896 array files hash to the values in the manifest. The report was written by the committed `f9_probe_report.py` (`1f2f8cfae79267fc…`).

**Discipline kept (declaration §4).** L1 computed only R-1 to R-8. No occupancy map was rendered or viewed, no statistic against λ contours was computed and no edge was extracted. The boundary-compatibility endpoint has not been seen. One further computation used the terrain arrays alone and no probe output (§4, item on TB).

## 2. The report

Columns are κ. Four seeds per configuration.

**R-1. Wall seconds per run (mean / max).**

| | realization | skeleton |
|---|---|---|
| L = 50 | 0.51 / 0.77 | 0.31 / 0.73 |
| L = 100 | 0.96 / 1.87 | 0.62 / 1.66 |

### L = 50

**R-2. Realization, mean tail density.**

| Arm | 0.75 | 1.00 | 1.25 | 1.50 | 1.75 | 2.00 | 2.50 | 3.00 |
|---|---|---|---|---|---|---|---|---|
| T0·P | 0.120 | 0.169 | 0.234 | 0.311 | 0.382 | 0.445 | 0.536 | 0.601 |
| TA·P | 0.071 | 0.082 | 0.095 | 0.112 | 0.129 | 0.150 | 0.189 | 0.227 |
| TA·H | 0.091 | 0.116 | 0.148 | 0.188 | 0.233 | 0.281 | 0.370 | 0.445 |
| TB·P | 0.086 | 0.106 | 0.135 | 0.169 | 0.204 | 0.239 | 0.303 | 0.361 |
| TB·H | 0.105 | 0.138 | 0.188 | 0.245 | 0.307 | 0.366 | 0.463 | 0.539 |
| TC·P | 0.114 | 0.157 | 0.215 | 0.285 | 0.352 | 0.410 | 0.501 | 0.565 |
| TC·H | 0.117 | 0.164 | 0.229 | 0.300 | 0.371 | 0.435 | 0.528 | 0.593 |

**R-2. Skeleton, mean tail density (survivors of 4).**

| Arm | 0.75 | 1.00 | 1.25 | 1.50 | 1.75 | 2.00 | 2.50 | 3.00 |
|---|---|---|---|---|---|---|---|---|
| T0·P | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.124 (4) | 0.301 (4) | 0.399 (4) | 0.516 (4) | 0.589 (4) |
| TA·P | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.022 (4) | 0.045 (4) | 0.086 (4) | 0.126 (4) |
| TA·H | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.001 (0) | 0.060 (4) | 0.128 (4) | 0.271 (4) | 0.381 (4) |
| TB·P | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.007 (1) | 0.085 (4) | 0.132 (4) | 0.211 (4) | 0.276 (4) |
| TB·H | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.011 (1) | 0.148 (4) | 0.248 (4) | 0.420 (4) | 0.515 (4) |
| TC·P | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.095 (4) | 0.256 (4) | 0.348 (4) | 0.470 (4) | 0.544 (4) |
| TC·H | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.097 (4) | 0.279 (4) | 0.378 (4) | 0.503 (4) | 0.579 (4) |

**R-3. Realization, W = 1 occupancy across cells: 5th / 50th / 95th percentile** (floor reference 0.0523).

| Arm | 0.75 | 1.00 | 1.25 | 1.50 | 1.75 | 2.00 | 2.50 | 3.00 |
|---|---|---|---|---|---|---|---|---|
| T0·P | 0.09 / 0.12 / 0.15 | 0.14 / 0.17 / 0.20 | 0.20 / 0.23 / 0.27 | 0.28 / 0.31 / 0.34 | 0.35 / 0.38 / 0.42 | 0.41 / 0.45 / 0.48 | 0.51 / 0.54 / 0.56 | 0.58 / 0.60 / 0.62 |
| TA·P | 0.04 / 0.07 / 0.11 | 0.05 / 0.07 / 0.15 | 0.05 / 0.08 / 0.21 | 0.05 / 0.09 / 0.27 | 0.05 / 0.10 / 0.34 | 0.05 / 0.11 / 0.40 | 0.06 / 0.13 / 0.50 | 0.06 / 0.16 / 0.58 |
| TA·H | 0.06 / 0.09 / 0.13 | 0.07 / 0.11 / 0.17 | 0.08 / 0.14 / 0.23 | 0.09 / 0.18 / 0.31 | 0.11 / 0.23 / 0.38 | 0.13 / 0.28 / 0.44 | 0.17 / 0.38 / 0.53 | 0.22 / 0.47 / 0.60 |
| TB·P | 0.05 / 0.08 / 0.13 | 0.05 / 0.10 / 0.18 | 0.06 / 0.11 / 0.25 | 0.07 / 0.14 / 0.32 | 0.07 / 0.17 / 0.40 | 0.08 / 0.20 / 0.46 | 0.09 / 0.28 / 0.55 | 0.11 / 0.37 / 0.61 |
| TB·H | 0.08 / 0.10 / 0.14 | 0.10 / 0.14 / 0.19 | 0.13 / 0.18 / 0.26 | 0.17 / 0.24 / 0.33 | 0.21 / 0.31 / 0.40 | 0.26 / 0.37 / 0.47 | 0.36 / 0.47 / 0.55 | 0.45 / 0.55 / 0.62 |
| TC·P | 0.08 / 0.12 / 0.14 | 0.09 / 0.16 / 0.20 | 0.10 / 0.23 / 0.27 | 0.13 / 0.30 / 0.34 | 0.15 / 0.38 / 0.41 | 0.18 / 0.44 / 0.47 | 0.24 / 0.53 / 0.56 | 0.31 / 0.59 / 0.62 |
| TC·H | 0.09 / 0.12 / 0.15 | 0.13 / 0.16 / 0.20 | 0.18 / 0.23 / 0.27 | 0.23 / 0.31 / 0.34 | 0.30 / 0.38 / 0.41 | 0.36 / 0.44 / 0.48 | 0.46 / 0.54 / 0.56 | 0.53 / 0.60 / 0.62 |

**R-4. Correlation between the P-arm and H-arm occupancy maps.**

| Arm | 0.75 | 1.00 | 1.25 | 1.50 | 1.75 | 2.00 | 2.50 | 3.00 |
|---|---|---|---|---|---|---|---|---|
| TA | 0.554 | 0.748 | 0.817 | 0.867 | 0.870 | 0.864 | 0.845 | 0.837 |
| TB | 0.551 | 0.736 | 0.856 | 0.890 | 0.913 | 0.929 | 0.940 | 0.945 |
| TC | 0.207 | 0.445 | 0.645 | 0.725 | 0.784 | 0.830 | 0.843 | 0.828 |

**R-5. TB: fraction of across-cell occupancy variance carried by the x-only means.**

| Arm | 0.75 | 1.00 | 1.25 | 1.50 | 1.75 | 2.00 | 2.50 | 3.00 |
|---|---|---|---|---|---|---|---|---|
| TB·P | 0.731 | 0.866 | 0.928 | 0.958 | 0.972 | 0.982 | 0.987 | 0.985 |
| TB·H | 0.407 | 0.660 | 0.809 | 0.876 | 0.915 | 0.916 | 0.922 | 0.916 |

**R-6. TC: occupancy inside the patch ÷ outside (inside, outside).**

| Arm | 0.75 | 1.00 | 1.25 | 1.50 | 1.75 | 2.00 | 2.50 | 3.00 |
|---|---|---|---|---|---|---|---|---|
| TC·P | 0.57 (0.068, 0.119) | 0.44 (0.074, 0.168) | 0.34 (0.079, 0.233) | 0.30 (0.094, 0.310) | 0.27 (0.104, 0.383) | 0.27 (0.120, 0.444) | 0.28 (0.149, 0.537) | 0.33 (0.196, 0.600) |
| TC·H | 0.83 (0.100, 0.120) | 0.75 (0.126, 0.168) | 0.70 (0.165, 0.236) | 0.68 (0.213, 0.311) | 0.71 (0.272, 0.382) | 0.72 (0.323, 0.447) | 0.79 (0.427, 0.538) | 0.85 (0.509, 0.601) |

**R-7. Seed-to-seed SD of tail density, realization.**

| Arm | 0.75 | 1.00 | 1.25 | 1.50 | 1.75 | 2.00 | 2.50 | 3.00 |
|---|---|---|---|---|---|---|---|---|
| T0·P | 0.0011 | 0.0024 | 0.0008 | 0.0020 | 0.0029 | 0.0020 | 0.0006 | 0.0007 |
| TA·P | 0.0005 | 0.0008 | 0.0008 | 0.0015 | 0.0013 | 0.0011 | 0.0009 | 0.0015 |
| TA·H | 0.0008 | 0.0010 | 0.0015 | 0.0018 | 0.0023 | 0.0005 | 0.0013 | 0.0014 |
| TB·P | 0.0005 | 0.0011 | 0.0022 | 0.0029 | 0.0002 | 0.0024 | 0.0010 | 0.0018 |
| TB·H | 0.0017 | 0.0011 | 0.0015 | 0.0021 | 0.0023 | 0.0024 | 0.0027 | 0.0017 |
| TC·P | 0.0007 | 0.0011 | 0.0016 | 0.0016 | 0.0011 | 0.0012 | 0.0006 | 0.0008 |
| TC·H | 0.0016 | 0.0021 | 0.0026 | 0.0017 | 0.0018 | 0.0026 | 0.0011 | 0.0003 |

**R-7. Seed-to-seed SD of tail density, skeleton.**

| Arm | 0.75 | 1.00 | 1.25 | 1.50 | 1.75 | 2.00 | 2.50 | 3.00 |
|---|---|---|---|---|---|---|---|---|
| T0·P | 0.0000 | 0.0000 | 0.0000 | 0.0078 | 0.0037 | 0.0009 | 0.0004 | 0.0010 |
| TA·P | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0018 | 0.0012 | 0.0033 | 0.0014 |
| TA·H | 0.0000 | 0.0000 | 0.0000 | 0.0015 | 0.0027 | 0.0049 | 0.0040 | 0.0029 |
| TB·P | 0.0000 | 0.0000 | 0.0000 | 0.0120 | 0.0020 | 0.0013 | 0.0024 | 0.0015 |
| TB·H | 0.0000 | 0.0000 | 0.0000 | 0.0147 | 0.0044 | 0.0031 | 0.0007 | 0.0026 |
| TC·P | 0.0000 | 0.0000 | 0.0000 | 0.0140 | 0.0051 | 0.0026 | 0.0024 | 0.0007 |
| TC·H | 0.0000 | 0.0000 | 0.0000 | 0.0086 | 0.0030 | 0.0014 | 0.0016 | 0.0010 |

### L = 100

**R-2. Realization, mean tail density.**

| Arm | 0.75 | 1.00 | 1.25 | 1.50 | 1.75 | 2.00 | 2.50 | 3.00 |
|---|---|---|---|---|---|---|---|---|
| T0·P | 0.119 | 0.168 | 0.235 | 0.311 | 0.383 | 0.444 | 0.537 | 0.601 |
| TA·P | 0.070 | 0.080 | 0.092 | 0.107 | 0.125 | 0.143 | 0.181 | 0.219 |
| TA·H | 0.090 | 0.113 | 0.143 | 0.182 | 0.226 | 0.272 | 0.359 | 0.436 |
| TB·P | 0.085 | 0.103 | 0.130 | 0.162 | 0.197 | 0.231 | 0.294 | 0.350 |
| TB·H | 0.104 | 0.138 | 0.184 | 0.241 | 0.302 | 0.361 | 0.460 | 0.534 |
| TC·P | 0.113 | 0.157 | 0.215 | 0.284 | 0.351 | 0.410 | 0.500 | 0.563 |
| TC·H | 0.117 | 0.163 | 0.227 | 0.300 | 0.371 | 0.434 | 0.527 | 0.591 |

**R-2. Skeleton, mean tail density (survivors of 4).**

| Arm | 0.75 | 1.00 | 1.25 | 1.50 | 1.75 | 2.00 | 2.50 | 3.00 |
|---|---|---|---|---|---|---|---|---|
| T0·P | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.123 (4) | 0.299 (4) | 0.398 (4) | 0.516 (4) | 0.588 (4) |
| TA·P | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.001 (1) | 0.018 (4) | 0.037 (4) | 0.075 (4) | 0.113 (4) |
| TA·H | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.005 (2) | 0.051 (4) | 0.110 (4) | 0.251 (4) | 0.362 (4) |
| TB·P | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.006 (2) | 0.069 (4) | 0.117 (4) | 0.196 (4) | 0.262 (4) |
| TB·H | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.029 (4) | 0.134 (4) | 0.234 (4) | 0.411 (4) | 0.510 (4) |
| TC·P | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.095 (4) | 0.252 (4) | 0.347 (4) | 0.467 (4) | 0.543 (4) |
| TC·H | 0.000 (0) | 0.000 (0) | 0.000 (0) | 0.097 (4) | 0.275 (4) | 0.379 (4) | 0.503 (4) | 0.578 (4) |

**R-3. Realization, W = 1 occupancy across cells: 5th / 50th / 95th percentile** (floor reference 0.0523).

| Arm | 0.75 | 1.00 | 1.25 | 1.50 | 1.75 | 2.00 | 2.50 | 3.00 |
|---|---|---|---|---|---|---|---|---|
| T0·P | 0.09 / 0.12 / 0.15 | 0.14 / 0.17 / 0.20 | 0.20 / 0.23 / 0.27 | 0.28 / 0.31 / 0.34 | 0.35 / 0.38 / 0.41 | 0.41 / 0.44 / 0.47 | 0.51 / 0.54 / 0.56 | 0.58 / 0.60 / 0.62 |
| TA·P | 0.04 / 0.07 / 0.11 | 0.05 / 0.07 / 0.15 | 0.05 / 0.08 / 0.20 | 0.05 / 0.08 / 0.26 | 0.05 / 0.09 / 0.33 | 0.05 / 0.10 / 0.39 | 0.05 / 0.12 / 0.49 | 0.06 / 0.15 / 0.56 |
| TA·H | 0.06 / 0.09 / 0.12 | 0.07 / 0.11 / 0.17 | 0.08 / 0.14 / 0.22 | 0.09 / 0.17 / 0.30 | 0.11 / 0.22 / 0.37 | 0.12 / 0.27 / 0.43 | 0.16 / 0.37 / 0.53 | 0.21 / 0.46 / 0.59 |
| TB·P | 0.05 / 0.08 / 0.13 | 0.05 / 0.09 / 0.17 | 0.06 / 0.11 / 0.24 | 0.06 / 0.13 / 0.31 | 0.07 / 0.16 / 0.38 | 0.07 / 0.19 / 0.45 | 0.09 / 0.27 / 0.54 | 0.10 / 0.35 / 0.60 |
| TB·H | 0.07 / 0.10 / 0.14 | 0.10 / 0.14 / 0.18 | 0.12 / 0.18 / 0.25 | 0.16 / 0.24 / 0.33 | 0.21 / 0.30 / 0.40 | 0.26 / 0.36 / 0.46 | 0.36 / 0.47 / 0.55 | 0.44 / 0.54 / 0.61 |
| TC·P | 0.07 / 0.12 / 0.14 | 0.09 / 0.16 / 0.20 | 0.10 / 0.23 / 0.26 | 0.12 / 0.30 / 0.34 | 0.15 / 0.37 / 0.41 | 0.17 / 0.44 / 0.47 | 0.24 / 0.53 / 0.56 | 0.31 / 0.59 / 0.62 |
| TC·H | 0.09 / 0.12 / 0.14 | 0.13 / 0.16 / 0.20 | 0.18 / 0.23 / 0.27 | 0.23 / 0.30 / 0.34 | 0.29 / 0.38 / 0.41 | 0.36 / 0.44 / 0.47 | 0.46 / 0.53 / 0.56 | 0.54 / 0.60 / 0.62 |

**R-4. Correlation between the P-arm and H-arm occupancy maps.**

| Arm | 0.75 | 1.00 | 1.25 | 1.50 | 1.75 | 2.00 | 2.50 | 3.00 |
|---|---|---|---|---|---|---|---|---|
| TA | 0.531 | 0.735 | 0.819 | 0.866 | 0.865 | 0.860 | 0.843 | 0.833 |
| TB | 0.523 | 0.726 | 0.847 | 0.895 | 0.908 | 0.925 | 0.933 | 0.943 |
| TC | 0.234 | 0.455 | 0.612 | 0.729 | 0.783 | 0.815 | 0.837 | 0.822 |

**R-5. TB: fraction of across-cell occupancy variance carried by the x-only means.**

| Arm | 0.75 | 1.00 | 1.25 | 1.50 | 1.75 | 2.00 | 2.50 | 3.00 |
|---|---|---|---|---|---|---|---|---|
| TB·P | 0.707 | 0.850 | 0.927 | 0.955 | 0.970 | 0.977 | 0.984 | 0.986 |
| TB·H | 0.388 | 0.647 | 0.811 | 0.884 | 0.908 | 0.923 | 0.925 | 0.918 |

**R-6. TC: occupancy inside the patch ÷ outside (inside, outside).**

| Arm | 0.75 | 1.00 | 1.25 | 1.50 | 1.75 | 2.00 | 2.50 | 3.00 |
|---|---|---|---|---|---|---|---|---|
| TC·P | 0.56 (0.067, 0.119) | 0.44 (0.073, 0.168) | 0.34 (0.079, 0.232) | 0.29 (0.089, 0.309) | 0.26 (0.101, 0.381) | 0.26 (0.115, 0.444) | 0.27 (0.147, 0.537) | 0.30 (0.182, 0.598) |
| TC·H | 0.80 (0.096, 0.119) | 0.72 (0.122, 0.168) | 0.69 (0.162, 0.235) | 0.68 (0.211, 0.310) | 0.70 (0.269, 0.382) | 0.73 (0.326, 0.445) | 0.80 (0.429, 0.537) | 0.85 (0.508, 0.600) |

**R-7. Seed-to-seed SD of tail density, realization.**

| Arm | 0.75 | 1.00 | 1.25 | 1.50 | 1.75 | 2.00 | 2.50 | 3.00 |
|---|---|---|---|---|---|---|---|---|
| T0·P | 0.0005 | 0.0004 | 0.0009 | 0.0010 | 0.0010 | 0.0001 | 0.0005 | 0.0004 |
| TA·P | 0.0003 | 0.0003 | 0.0005 | 0.0004 | 0.0005 | 0.0009 | 0.0006 | 0.0007 |
| TA·H | 0.0005 | 0.0005 | 0.0004 | 0.0003 | 0.0008 | 0.0006 | 0.0009 | 0.0011 |
| TB·P | 0.0004 | 0.0007 | 0.0004 | 0.0013 | 0.0006 | 0.0008 | 0.0008 | 0.0005 |
| TB·H | 0.0004 | 0.0005 | 0.0008 | 0.0006 | 0.0011 | 0.0010 | 0.0007 | 0.0009 |
| TC·P | 0.0008 | 0.0009 | 0.0011 | 0.0007 | 0.0009 | 0.0004 | 0.0006 | 0.0003 |
| TC·H | 0.0005 | 0.0002 | 0.0005 | 0.0009 | 0.0009 | 0.0008 | 0.0008 | 0.0006 |

**R-7. Seed-to-seed SD of tail density, skeleton.**

| Arm | 0.75 | 1.00 | 1.25 | 1.50 | 1.75 | 2.00 | 2.50 | 3.00 |
|---|---|---|---|---|---|---|---|---|
| T0·P | 0.0000 | 0.0000 | 0.0000 | 0.0063 | 0.0011 | 0.0006 | 0.0008 | 0.0006 |
| TA·P | 0.0000 | 0.0000 | 0.0000 | 0.0023 | 0.0002 | 0.0012 | 0.0009 | 0.0014 |
| TA·H | 0.0000 | 0.0000 | 0.0000 | 0.0053 | 0.0025 | 0.0026 | 0.0012 | 0.0009 |
| TB·P | 0.0000 | 0.0000 | 0.0000 | 0.0041 | 0.0009 | 0.0023 | 0.0016 | 0.0008 |
| TB·H | 0.0000 | 0.0000 | 0.0000 | 0.0046 | 0.0028 | 0.0009 | 0.0012 | 0.0009 |
| TC·P | 0.0000 | 0.0000 | 0.0000 | 0.0065 | 0.0019 | 0.0008 | 0.0005 | 0.0006 |
| TC·H | 0.0000 | 0.0000 | 0.0000 | 0.0059 | 0.0015 | 0.0006 | 0.0006 | 0.0003 |

**R-8. Validity of the flicker record.** Range violations: 0. Cell-records in all: 5,600,000; in extinct skeleton runs: 1,155,000.

| W | all-active cell-records | all-inactive cell-records |
|---|---|---|
| 1 | 0 | 1,529,853 |
| 10 | 17,380 | 1,529,853 |
| 100 | 2,905,642 | 1,529,853 |

## 3. What was learned (descriptive; four seeds)

1. **Cost.** A realization run takes about 0.5 s at L = 50 and 1.0 s at L = 100. The larger lattice costs about twice as much, not four times.
2. **Skeleton persistence.** On the flat arm the skeleton is extinct in all seeds at κ ≤ 1.25 and survives in all at κ = 1.50. On every terrain arm it is extinct in all seeds at κ ≤ 1.25 and survives in all by κ = 1.75. Under the spectral normalization the terrain arms' thresholds fall in the same κ band as the flat lattice's. This is a fidelity-kind observation at four seeds and eight levels, nothing more.
3. **Range.** Realization occupancy runs from near the floor to about 0.62 over the κ grid; nothing saturates.
4. **TC gives the two rules different spatial output.** The inside-to-outside occupancy ratio is 0.26–0.34 under the product rule and 0.68–0.73 under the height rule for κ from 1.25 to 2.00, at both sizes.
5. **TB, as specified, does not.** The P-arm and H-arm maps correlate no less on TB than on the concordant control TA, and the x-only variance fraction is higher for the product arm than for the height arm.
6. **Noise.** Seed-to-seed SD of realization tail density is at most 0.003 at L = 50 and 0.0013 at L = 100; for the skeleton next to its threshold it reaches 0.015.
7. **Flicker record.** The record is produced correctly. At W = 100 most cell-records of non-extinct runs are active in all ten windows, so the declared statistic returns "undefined: no inactive segment" for most cells at that window with a 1,000-tick tail.

## 4. An error of L1's in the terrain specification

Terrain TB was meant to give the product and the height different contours. Computed from the terrain arrays alone (no probe output): 99.32% of the product's across-cell variance on TB lies along x, the axis on which the height varies (100.00%). The imbalance axis was specified far too weak. L1 could and should have computed this before the declaration; it needs no run. Why the height arm's x-only fraction (R-5) is below the product arm's is not established; per-cell sampling noise against the height arm's smaller contrast is a likely explanation only.

## 5. Changes, ruled by Mike 2026-11-12 ("accepted")

Each is a cost, feasibility or terrain change. None alters the claim grammar of declaration §1, the outcome labels, the normalization, or any contour, edge, tolerance or aggregation rule.

| # | Change | Kind | Basis |
|---|---|---|---|
| 1 | L = 100 for the contract | cost | R-1, R-7 |
| 2 | A finer κ grid between 1.0 and 2.0, range kept to 3.0 | feasibility | R-2 |
| 3 | TB respecified by terrain arithmetic so that the product's variation is shared comparably between the two axes, checked from the arrays before any run. No second probe; the canonical run meets the new TB fresh. | terrain | R-4, R-5, §4 |
| 4 | T0, TA and TC kept as specified | terrain | R-6 |
| 5 | The flicker window set is left as declared; the W = 100 saturation is recorded | — | R-8 |

**Selection, disclosed (declaration §4).** TC is kept and TB is changed because of what this probe showed. Later inference on these terrains is conditional on that selection: fresh canonical seeds can replicate a response on them, and cannot make the contrast an unanticipated finding or show generality across terrains.

## 6. What this record is not

Not a result of Flight 9. Canonical work uses fresh masters; the probe master 9920261112 is retired. Probe output is never relabeled as calibration, held-out qualification or canonical observation.

*L1, 2026-11-12.*
