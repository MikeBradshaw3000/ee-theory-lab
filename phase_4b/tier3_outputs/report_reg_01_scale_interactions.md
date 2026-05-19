# Tier 3 Regression Report: reg_01_scale_interactions

### Interpretation Boundary

#### What this regression licenses

1. Quantification of F-form main effect on logit(p_base) at the cellular
   level.


#### What this regression does not adjudicate

1. Architectural selection of F_LR vs F_2_symmetric for Open Element 14.

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
Method:                 Least Squares   F-statistic:                 2.275e-13
Date:                Sun, 17 May 2026   Prob (F-statistic):               1.00
Time:                        20:49:56   Log-Likelihood:             1.0267e+08
No. Observations:            12000000   AIC:                        -2.053e+08
Df Residuals:                11999979   BIC:                        -2.053e+08
Df Model:                          20                                         
Covariance Type:              cluster                                         
==========================================================================================================
                                             coef    std err          z      P>|z|      [0.025      0.975]
----------------------------------------------------------------------------------------------------------
Intercept                                 -4.0000        nan        nan        nan         nan         nan
C(F_variant)[T.F_LR]                    1.146e-14      0.359   3.19e-14      1.000      -0.704       0.704
C(scale)[T.40x40]                      -3.546e-14      0.004  -7.99e-12      1.000      -0.009       0.009
C(epoch)[T.1]                          -3.993e-14        nan        nan        nan         nan         nan
C(epoch)[T.2]                           3.003e-15      0.029   1.02e-13      1.000      -0.058       0.058
C(epoch)[T.3]                           -3.15e-14        nan        nan        nan         nan         nan
C(epoch)[T.4]                          -1.565e-14        nan        nan        nan         nan         nan
C(epoch)[T.5]                          -3.623e-14      0.109  -3.31e-13      1.000      -0.214       0.214
C(epoch)[T.6]                          -3.276e-14      0.094  -3.47e-13      1.000      -0.185       0.185
C(scale)[T.40x40]:C(F_variant)[T.F_LR] -1.156e-14      0.005  -2.49e-12      1.000      -0.009       0.009
Lambda_total                               0.0038   2.69e+10   1.42e-13      1.000   -5.27e+10    5.27e+10
Local_Density                             -0.0551   2.83e+13  -1.95e-15      1.000   -5.55e+13    5.55e+13
Local_Density_squared                     -0.2347    3.3e+10  -7.12e-12      1.000   -6.46e+10    6.46e+10
Term_Lambda                                0.9990   6.73e+09   1.49e-10      1.000   -1.32e+10    1.32e+10
Term_Density_Pos                           1.0184    6.9e+12   1.48e-13      1.000   -1.35e+13    1.35e+13
Term_Overcrowding                          0.9413      9e+09   1.05e-10      1.000   -1.76e+10    1.76e+10
Psi_local                               9.688e-16      0.000   3.73e-12      1.000      -0.001       0.001
b_i_v                                   5.014e-15      0.005   9.16e-13      1.000      -0.011       0.011
b_i_u                                   3.205e-15      0.002   1.45e-12      1.000      -0.004       0.004
b_i_r                                    3.64e-15      0.001   2.81e-12      1.000      -0.003       0.003
rho_global                              6.301e-15      0.039    1.6e-13      1.000      -0.077       0.077
C(scale)[T.40x40]:rho_global            6.361e-14      0.015   4.21e-12      1.000      -0.030       0.030
psi_global                              1.193e-15      0.081   1.47e-14      1.000      -0.159       0.159
C(scale)[T.40x40]:psi_global           -4.948e-16      0.077  -6.42e-15      1.000      -0.151       0.151
==============================================================================
Omnibus:                    25192.941   Durbin-Watson:                   0.371
Prob(Omnibus):                  0.000   Jarque-Bera (JB):            31296.434
Skew:                           0.025   Prob(JB):                         0.00
Kurtosis:                       3.245   Cond. No.                     2.61e+15
==============================================================================

Notes:
[1] Standard Errors are robust to cluster correlation (cluster)
[2] The smallest eigenvalue is 1.45e-23. This might indicate that there are
strong multicollinearity problems or that the design matrix is singular.
```

### Sensitivity analysis (NOT the primary uncertainty method)

#### Clustered by: cell

```
                            OLS Regression Results                            
==============================================================================
Dep. Variable:           logit_p_base   R-squared:                       1.000
Model:                            OLS   Adj. R-squared:                  1.000
Method:                 Least Squares   F-statistic:                 8.773e-14
Date:                Sun, 17 May 2026   Prob (F-statistic):               1.00
Time:                        20:49:58   Log-Likelihood:             1.0267e+08
No. Observations:            12000000   AIC:                        -2.053e+08
Df Residuals:                11999979   BIC:                        -2.053e+08
Df Model:                          20                                         
Covariance Type:              cluster                                         
==========================================================================================================
                                             coef    std err          z      P>|z|      [0.025      0.975]
----------------------------------------------------------------------------------------------------------
Intercept                                 -4.0000      0.134    -29.804      0.000      -4.263      -3.737
C(F_variant)[T.F_LR]                    1.146e-14        nan        nan        nan         nan         nan
C(scale)[T.40x40]                      -3.546e-14        nan        nan        nan         nan         nan
C(epoch)[T.1]                          -3.993e-14        nan        nan        nan         nan         nan
C(epoch)[T.2]                           3.003e-15        nan        nan        nan         nan         nan
C(epoch)[T.3]                           -3.15e-14        nan        nan        nan         nan         nan
C(epoch)[T.4]                          -1.565e-14        nan        nan        nan         nan         nan
C(epoch)[T.5]                          -3.623e-14        nan        nan        nan         nan         nan
C(epoch)[T.6]                          -3.276e-14        nan        nan        nan         nan         nan
C(scale)[T.40x40]:C(F_variant)[T.F_LR] -1.156e-14        nan        nan        nan         nan         nan
Lambda_total                               0.0038   6.58e+10    5.8e-14      1.000   -1.29e+11    1.29e+11
Local_Density                             -0.0551        nan        nan        nan         nan         nan
Local_Density_squared                     -0.2347        nan        nan        nan         nan         nan
Term_Lambda                                0.9990   3.83e+10   2.61e-11      1.000    -7.5e+10     7.5e+10
Term_Density_Pos                           1.0184        nan        nan        nan         nan         nan
Term_Overcrowding                          0.9413        nan        nan        nan         nan         nan
Psi_local                               9.688e-16        nan        nan        nan         nan         nan
b_i_v                                   5.014e-15        nan        nan        nan         nan         nan
b_i_u                                   3.205e-15        nan        nan        nan         nan         nan
b_i_r                                    3.64e-15        nan        nan        nan         nan         nan
rho_global                              6.301e-15        nan        nan        nan         nan         nan
C(scale)[T.40x40]:rho_global            6.361e-14        nan        nan        nan         nan         nan
psi_global                              1.193e-15        nan        nan        nan         nan         nan
C(scale)[T.40x40]:psi_global           -4.948e-16        nan        nan        nan         nan         nan
==============================================================================
Omnibus:                    25192.941   Durbin-Watson:                   0.371
Prob(Omnibus):                  0.000   Jarque-Bera (JB):            31296.434
Skew:                           0.025   Prob(JB):                         0.00
Kurtosis:                       3.245   Cond. No.                     2.61e+15
==============================================================================

Notes:
[1] Standard Errors are robust to cluster correlation (cluster)
[2] The smallest eigenvalue is 1.45e-23. This might indicate that there are
strong multicollinearity problems or that the design matrix is singular.
```

### Classification Status

> Classification fields are intentionally left blank for post-output review. 
Tier 3 estimates inform classification but do not assign structural status automatically. 
Classification is performed by Mike or routed AI review against the registered interpretation_boundary.
