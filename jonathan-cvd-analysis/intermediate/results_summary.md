# Jonathan's CVD Analysis — Results Summary

Generated: 2026-03-29

## Model Performance (LOOCV)

| Target | Model | R-squared | RMSE | Notes |
|--------|-------|-----------|------|-------|
| Heart Disease Mortality | Linear Regression | 0.5299 | 22.44 | Best LR model |
| Heart Disease Mortality | KNN (k=7) | 0.6473 | 19.44 | Best overall model |
| Coronary Heart Mortality | Linear Regression | 0.4996 | 12.82 | |
| Coronary Heart Mortality | KNN (k=8) | 0.3377 | 14.75 | LR beats KNN here |
| Stroke Mortality | Linear Regression | 0.1068 | 7.34 | Hardest to predict |
| Stroke Mortality | KNN (k=7) | 0.2682 | 6.64 | |
| Diabetes Prevalence | Linear Regression | 0.6848 | 1.03 | Cross-disease comparison |

## Top Predictors (Heart Disease Mortality, Standardized Coefficients)

1. poverty_prev: 13.45
2. obesity_prev: 10.71
3. food_insecurity_prev: 7.01
4. hs_completion_prev: 6.34
5. smoking_prev: 3.17

## Key Findings

- **Poverty is the strongest predictor** of heart disease mortality at the state level, stronger than traditional risk factors like smoking
- **KNN outperforms linear regression** for heart disease mortality (R²=0.65 vs 0.53), suggesting nonlinear relationships
- **Stroke mortality is poorly predicted** by these risk factors (R²=0.11-0.27), suggesting other drivers dominate
- **Adding insurance data does NOT improve prediction** (R² drops from 0.43 to 0.41 on 35-state subset) — but 31% missing data limits this conclusion
- **Same predictors work better for diabetes** (R²=0.68) than heart disease (R²=0.53), suggesting diabetes has more direct lifestyle-factor drivers
- **Strong geographic clustering**: Southeast "stroke belt" visible in choropleths, overlapping with poverty patterns
- **Poverty t-test**: States above median poverty have significantly higher heart disease mortality (p < 0.0001)

## Social Determinants Finding

The insurance variable (uninsured_prev) has too much missing data (16/51 states) to draw strong conclusions. However, poverty_prev is the single strongest predictor of heart disease mortality — stronger than smoking, obesity, or physical inactivity — supporting the social determinants hypothesis.
