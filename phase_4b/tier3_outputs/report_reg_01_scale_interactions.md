# Tier 3 Regression Report: reg_01_scale_interactions

### Interpretation Boundary

#### What this regression licenses

1. Quantification of F-form main effect on logit(p_base) at the cellular
   level, controlling for density pathway, base structure, Psi_local, and
   epoch.
2. Quantification of scale main effect on logit(p_base) at the cellular
   level, similarly controlled.
3. Test of scale-stability of F-form effect via the scale x F_variant
   interaction term: small/null interaction supports scale-stable
   characterization (yesterday's Tier 2 cross-scale verdict).
4. Test of scale-dependence of population-level density (rho_global) and
   coherence (psi_global) effects via scale x rho_global and scale x
   psi_global.
5. Two-field classification of each estimated effect per Phase 4B spec
   Section 6.


#### What this regression does not adjudicate

1. Architectural selection of F_LR vs F_2_symmetric for Open Element 14.
   Per Phase 4B spec Section 6.4: F-form selection is structural_status =
   open_element_not_resolved regardless of regression results.
2. Finite-size scaling functional form. Two scales is insufficient per
   Section 5.3; this is outside_phase_4b_scope.
3. PRNG-realization variance. Matched-seed design; this is
   requires_additional_probe (Flight 3a-style).
4. Causal interpretation of any coefficient. Per Phase 4B spec Section
   4.6: Tier 3 describes statistical structure in the Flight 2 record;
   the record was produced by known mechanisms, so coefficient signs
   trace to mechanisms by construction, not by causal inference.


### Dataset Details

- **Files loaded:** flight6_probe1_overcrowding_20x20.parquet, flight6_probe1_overcrowding_40x40.parquet, flight6_probe2_starvation_FLR_20x20.parquet, flight6_probe2_starvation_FLR_40x40.parquet
- **Independent runs:** 4
- **Primary Cluster Count (run_x_tick):** 12000

- **Eta-Boundary Count:** 0 / 12000000

> **CAVEAT:** Run-level replication is weak.

### Primary Model Results

```
                            OLS Regression Results                            
==============================================================================
Dep. Variable:           logit_p_base   R-squared:                       1.000
Model:                            OLS   Adj. R-squared:                  1.000
Method:                 Least Squares   F-statistic:                 1.212e-15
Date:                Wed, 20 May 2026   Prob (F-statistic):               1.00
Time:                        00:11:25   Log-Likelihood:             9.4034e+07
No. Observations:            12000000   AIC:                        -1.881e+08
Df Residuals:                11999979   BIC:                        -1.881e+08
Df Model:                          20                                         
Covariance Type:              cluster                                         
==========================================================================================================
                                             coef    std err          z      P>|z|      [0.025      0.975]
----------------------------------------------------------------------------------------------------------
Intercept                                 -4.0000        nan        nan        nan         nan         nan
C(F_variant)[T.F_LR]                    -9.59e-15      1.292  -7.42e-15      1.000      -2.533       2.533
C(scale)[T.40x40]                      -4.115e-14        nan        nan        nan         nan         nan
C(epoch)[T.1]                          -3.927e-14      0.048  -8.18e-13      1.000      -0.094       0.094
C(epoch)[T.2]                           6.327e-15        nan        nan        nan         nan         nan
C(epoch)[T.3]                          -3.887e-14      0.151  -2.58e-13      1.000      -0.296       0.296
C(epoch)[T.4]                          -1.093e-14        nan        nan        nan         nan         nan
C(epoch)[T.5]                          -2.591e-14        nan        nan        nan         nan         nan
C(epoch)[T.6]                          -2.177e-14        nan        nan        nan         nan         nan
C(scale)[T.40x40]:C(F_variant)[T.F_LR] -5.206e-15        nan        nan        nan         nan         nan
Lambda_total                               0.0038        nan        nan        nan         nan         nan
Local_Density                             -0.0550   9.69e+13  -5.68e-16      1.000    -1.9e+14     1.9e+14
Local_Density_squared                     -0.2355   8.35e+09  -2.82e-11      1.000   -1.64e+10    1.64e+10
Term_Lambda                                0.9991   8.23e+10   1.21e-11      1.000   -1.61e+11    1.61e+11
Term_Density_Pos                           1.0184   3.02e+13   3.38e-14      1.000   -5.91e+13    5.91e+13
Term_Overcrowding                          0.9411   2.09e+09   4.51e-10      1.000   -4.09e+09    4.09e+09
Psi_local                               6.892e-16   2.99e-05    2.3e-11      1.000   -5.87e-05    5.87e-05
b_i_v                                   5.894e-15      0.024   2.43e-13      1.000      -0.048       0.048
b_i_u                                  -4.459e-16      0.042  -1.07e-14      1.000      -0.081       0.081
b_i_r                                   1.028e-14      0.054    1.9e-13      1.000      -0.106       0.106
rho_global                               5.25e-14      0.075   7.02e-13      1.000      -0.147       0.147
C(scale)[T.40x40]:rho_global           -4.262e-14      0.073  -5.86e-13      1.000      -0.143       0.143
psi_global                              2.652e-15      0.442   5.99e-15      1.000      -0.867       0.867
C(scale)[T.40x40]:psi_global           -3.039e-15      0.535  -5.68e-15      1.000      -1.049       1.049
==============================================================================
Omnibus:                   782240.367   Durbin-Watson:                   0.114
Prob(Omnibus):                  0.000   Jarque-Bera (JB):           841586.943
Skew:                          -0.615   Prob(JB):                         0.00
Kurtosis:                       2.590   Cond. No.                     2.59e+15
==============================================================================

Notes:
[1] Standard Errors are robust to cluster correlation (cluster)
[2] The smallest eigenvalue is 1.47e-23. This might indicate that there are
strong multicollinearity problems or that the design matrix is singular.
```

### Sensitivity analysis (NOT the primary uncertainty method)

#### Clustered by: cell

```
                            OLS Regression Results                            
==============================================================================
Dep. Variable:           logit_p_base   R-squared:                       1.000
Model:                            OLS   Adj. R-squared:                  1.000
Method:                 Least Squares   F-statistic:                 1.084e-16
Date:                Wed, 20 May 2026   Prob (F-statistic):               1.00
Time:                        00:11:27   Log-Likelihood:             9.4034e+07
No. Observations:            12000000   AIC:                        -1.881e+08
Df Residuals:                11999979   BIC:                        -1.881e+08
Df Model:                          20                                         
Covariance Type:              cluster                                         
==========================================================================================================
                                             coef    std err          z      P>|z|      [0.025      0.975]
----------------------------------------------------------------------------------------------------------
Intercept                                 -4.0000        nan        nan        nan         nan         nan
C(F_variant)[T.F_LR]                    -9.59e-15        nan        nan        nan         nan         nan
C(scale)[T.40x40]                      -4.115e-14      0.008   -5.4e-12      1.000      -0.015       0.015
C(epoch)[T.1]                          -3.927e-14        nan        nan        nan         nan         nan
C(epoch)[T.2]                           6.327e-15        nan        nan        nan         nan         nan
C(epoch)[T.3]                          -3.887e-14        nan        nan        nan         nan         nan
C(epoch)[T.4]                          -1.093e-14      0.171  -6.38e-14      1.000      -0.336       0.336
C(epoch)[T.5]                          -2.591e-14      0.230  -1.13e-13      1.000      -0.451       0.451
C(epoch)[T.6]                          -2.177e-14      0.432  -5.04e-14      1.000      -0.847       0.847
C(scale)[T.40x40]:C(F_variant)[T.F_LR] -5.206e-15        nan        nan        nan         nan         nan
Lambda_total                               0.0038   6.36e+11   5.96e-15      1.000   -1.25e+12    1.25e+12
Local_Density                             -0.0550   6.91e+13  -7.96e-16      1.000   -1.35e+14    1.35e+14
Local_Density_squared                     -0.2355   1.32e+10  -1.78e-11      1.000   -2.59e+10    2.59e+10
Term_Lambda                                0.9991        nan        nan        nan         nan         nan
Term_Density_Pos                           1.0184        nan        nan        nan         nan         nan
Term_Overcrowding                          0.9411        nan        nan        nan         nan         nan
Psi_local                               6.892e-16   5.32e-05    1.3e-11      1.000      -0.000       0.000
b_i_v                                   5.894e-15        nan        nan        nan         nan         nan
b_i_u                                  -4.459e-16        nan        nan        nan         nan         nan
b_i_r                                   1.028e-14        nan        nan        nan         nan         nan
rho_global                               5.25e-14        nan        nan        nan         nan         nan
C(scale)[T.40x40]:rho_global           -4.262e-14        nan        nan        nan         nan         nan
psi_global                              2.652e-15        nan        nan        nan         nan         nan
C(scale)[T.40x40]:psi_global           -3.039e-15        nan        nan        nan         nan         nan
==============================================================================
Omnibus:                   782240.367   Durbin-Watson:                   0.114
Prob(Omnibus):                  0.000   Jarque-Bera (JB):           841586.943
Skew:                          -0.615   Prob(JB):                         0.00
Kurtosis:                       2.590   Cond. No.                     2.59e+15
==============================================================================

Notes:
[1] Standard Errors are robust to cluster correlation (cluster)
[2] The smallest eigenvalue is 1.47e-23. This might indicate that there are
strong multicollinearity problems or that the design matrix is singular.
```

### Classification Status

> Classification fields are intentionally left blank for post-output review. 
Tier 3 estimates inform classification but do not assign structural status automatically. 
Classification is performed by Mike or routed AI review against the registered interpretation_boundary.
