# Plan: Jonathan's CVD + Social Determinants Analysis

## Context

Jonathan's individual contribution to the DS2500 group project. The team analyzes state-level chronic disease indicators from the CDC. Jonathan's assignment: **cardiovascular disease** and **social determinants of health (insurance)**. Data pipeline is complete (`data/processed/state_indicators.csv` — 51 rows x 29 columns). No analysis notebooks exist yet. Deadline: 4/13 for project, 4/21 for final deliverables.

## Key Constraint: Small Sample Size (n=51)

Every modeling decision must account for only having 51 states:
- **LOOCV** instead of train/test split (15-state test set would be too noisy)
- **Max 5-7 predictors** per model to avoid overfitting
- **KNN k >= 5** (k=1-2 will overfit)
- No polynomial features, interaction terms, or regularization (not enough data, and beyond course scope)

## Key Constraint: Missing Data

- `uninsured_prev`: 16 states missing (31%) — run primary models without it, secondary analysis on 35-state subset
- `lack_social_support_prev`: 16 states missing (31%) — same treatment
- Do NOT impute — 31% missing on 51 obs would introduce too much noise

## Column Assignments

**Targets (cardiovascular):** `heart_disease_mortality_rate`, `coronary_heart_mortality_rate`, `stroke_mortality_rate`, `high_blood_pressure_prev`, `high_cholesterol_prev`

**Social determinant columns:** `uninsured_prev`, `poverty_prev`, `hs_completion_prev`, `food_insecurity_prev`, `lack_social_support_prev`

**Predictors:** `smoking_prev`, `obesity_prev`, `physical_inactivity_prev`, `flu_vaccination_prev`, `poverty_prev`, `hs_completion_prev`, `food_insecurity_prev` (7 predictors on 50 states, dropping FL for 1-missing columns)

**Off-limits as targets** (other members): diabetes (Min Yu), depression/alcohol (Anuhya), cancer/COPD (Tsion). `diabetes_prev` used only for cross-disease comparison.

---

## Implementation Steps

### File to create
`notebooks/jonathan_cvd_social_determinants.ipynb` — single notebook with markdown section headers

### Phase 1: EDA (3/29-3/30)

**A. Setup & Data Loading**
- Import: pandas, numpy, matplotlib, seaborn, plotly.express, sklearn, scipy.stats
- Load `../data/processed/state_indicators.csv`
- Print shape, dtypes, `.describe()` for Jonathan's columns
- Document missing data explicitly

**B. Distributions**
- Histograms + box plots for 5 cardiovascular columns (2x3 subplot grid)
- Shapiro-Wilk normality tests
- Same for social determinant columns (note 35-state subset for uninsured/social support)

**C. Correlation Analysis**
- Correlation heatmap: all ~14 Jonathan-relevant columns (`seaborn.heatmap`, annotated)
- Top 4-6 scatter plots with regression lines (`seaborn.regplot`), annotated with Pearson r and p-value
- Pearson + Spearman correlation table for each predictor vs `heart_disease_mortality_rate`
- Two-sample t-test: above-median vs below-median poverty states' heart disease rates

### Phase 2: Geographic Visualizations (3/30-3/31)

**D. Choropleth Maps**
- `heart_disease_mortality_rate` by state (`plotly.express.choropleth`, USA scope)
- `poverty_prev` by state (different color scale)
- `uninsured_prev` by state (35 states, missing = gray — itself informative)
- Side-by-side comparison showing geographic overlap (stroke belt visible in Southeast)

### Phase 3: Linear Regression (3/31-4/5)

**E. Primary Model**
- Target: `heart_disease_mortality_rate`
- 7 predictors (complete-data columns), StandardScaler
- LOOCV: report mean R-squared and RMSE
- Full-dataset fit: report coefficients, identify top predictors
- Residual diagnostics: residuals vs fitted, Q-Q plot

**F. Secondary Cardiovascular Models**
- Same predictor set for `stroke_mortality_rate` and `coronary_heart_mortality_rate`
- Compare R-squared across targets

**G. Social Determinants Model (35-state subset)**
- Add `uninsured_prev` as 8th predictor
- Re-run LOOCV on 35 states
- Key question: does adding insurance improve prediction?

### Phase 4: KNN Regression (4/3-4/7)

**H. KNN Tuning**
- Target: `heart_disease_mortality_rate`, same predictors, StandardScaler
- Tune k from 1-15 via LOOCV, plot RMSE vs k
- Report optimal k, R-squared, RMSE

**I. KNN for Other Targets**
- Repeat for `stroke_mortality_rate`, `coronary_heart_mortality_rate`

**J. Model Comparison Table**
| Target | Model | LOOCV R-squared | LOOCV RMSE | Top Predictors |
|--------|-------|-----------------|------------|----------------|
| heart_disease_mortality | LinReg | ? | ? | ? |
| heart_disease_mortality | KNN | ? | ? | ? |
| stroke_mortality | LinReg | ? | ? | ? |
| ... | ... | ... | ... | ... |

### Phase 5: Cross-Disease Comparison (4/7-4/10)

**K. Diabetes Comparison Model**
- Same predictor set, target = `diabetes_prev`
- LOOCV R-squared and coefficients
- Bar chart: standardized coefficients for heart disease model vs diabetes model side-by-side
- Narrative: which predictors differ between diseases?

### Phase 6: Comorbidity Analysis (4/7-4/10)

**L. Risk Tier Categorization**
- Median-split states into high/low for `heart_disease_mortality_rate` x `poverty_prev` (2x2 table)
- Chi-squared or Fisher's exact test
- List states in each quadrant
- Repeat for `food_insecurity_prev` and `uninsured_prev` (35-state)

**M. Cardiovascular Subtype Comorbidity**
- Scatter: `heart_disease_mortality_rate` vs `stroke_mortality_rate`, colored by `poverty_prev`
- Correlation between cardiovascular outcomes

### Phase 7: Ethical Considerations (4/10)

**N. Markdown cell addressing:**
1. **Ecological fallacy** — state-level correlations != individual causation
2. **Missing data bias** — 16 states missing insurance data are not random (Medicaid expansion timing)
3. **Confounders** — age, race, urbanization not in dataset but drive both CVD and poverty
4. **Labeling/stigma** — frame around systemic factors, not state identity
5. **Policy implications** — correlation != causation for insurance-mortality relationship

### Phase 8: Polish & Deliverables (4/11-4/12)

**O. Final Report Inputs**
- Summary table of all model results
- Select 3-4 best visualizations: (1) correlation heatmap, (2) choropleth, (3) strongest scatter plot, (4) coefficient comparison bar chart
- Slide content for 1-2 slides in team presentation

---

## Timeline

| Date | Work | Sections |
|------|------|----------|
| 3/29 | Data loaded, distributions, heatmap | A, B, C |
| 3/30 | Scatter plots, stats tests, choropleths | C (cont), D |
| 3/31 | First linear regression, Milestone 3 input | E |
| 4/1-4/4 | Remaining regressions, start KNN | F, G, H |
| 4/5-4/7 | KNN complete, cross-disease comparison | I, J, K |
| 4/8-4/10 | Comorbidity, ethics | L, M, N |
| 4/11-4/12 | Polish, summary table, slides | O |
| 4/13 | Practice meeting, deadline | -- |

## Risks

| Risk | Mitigation |
|------|-----------|
| `uninsured_prev` 31% missing | Primary models without it; secondary 35-state analysis; discuss limitation |
| Low R-squared | Expected with n=51. R-squared 0.4-0.6 is legitimate. Frame as "explains X% of variation" |
| Multicollinearity (smoking, obesity, poverty correlated) | Report correlation matrix, interpret coefficients cautiously, overall R-squared still valid |
| Overlap with Min Yu | Use obesity only as predictor, diabetes model only for comparison |

## Verification

- All LOOCV scores computed (no data leakage from fitting on full dataset then evaluating on same data)
- All visualizations render correctly in notebook
- Missing data documented and handled explicitly (no silent drops)
- Ethical considerations section written
- Model comparison table complete
- Notebook runs end-to-end from clean kernel (Restart & Run All)

## Critical Files

- `data/processed/state_indicators.csv` — single data source
- `notebooks/data_processing.ipynb` — reference for column derivation
- `notebooks/jonathan_cvd_social_determinants.ipynb` — TO CREATE
- `tasks/jonathan-cvd-analysis/` — intermediate context storage
