import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import StandardScaler

# 1. Loading clean data
df_clean = pd.read_csv("cleaned_chronic_disease_data.csv")

# 2. Filtering and structuring
# Filtering strictly for cancer and COPD + Tobacco as the predictor
research_df = df_clean[
    (df_clean['Topic'].isin(['Cancer', 'Tobacco', 'Chronic Obstructive Pulmonary Disease'])) & 
    (df_clean['DataValueType'].str.contains('Prevalence', na=False)) & 
    (df_clean['DataValue'] < 100)
].copy()

# Make every row state/year, with columns for the diseases and tobacco
final_table = research_df.pivot_table(
    index=['LocationDesc', 'YearStart'], 
    columns='Topic', 
    values='DataValue'
).dropna()

# 3. Model #1 Tobacco vs cancerr
# ==========================================
Xc = final_table[['Tobacco']]
yc = final_table['Cancer']

scaler_c = StandardScaler()
Xc_scaled = scaler_c.fit_transform(Xc)
Xc_train, Xc_test, yc_train, yc_test = train_test_split(Xc_scaled, yc, test_size=0.2, random_state=42)

lr_cancer = LinearRegression()
lr_cancer.fit(Xc_train, yc_train)

knn_cancer = KNeighborsRegressor(n_neighbors=5)
knn_cancer.fit(Xc_train, yc_train)

# 4. Model 2: Tobacco vs COPD
# ==========================================
Xcopd = final_table[['Tobacco']]
ycopd = final_table['Chronic Obstructive Pulmonary Disease']

scaler_copd = StandardScaler()
Xcopd_scaled = scaler_copd.fit_transform(Xcopd)
Xcopd_train, Xcopd_test, ycopd_train, ycopd_test = train_test_split(Xcopd_scaled, ycopd, test_size=0.2, random_state=42)

lr_copd = LinearRegression()
lr_copd.fit(Xcopd_train, ycopd_train)

knn_copd = KNeighborsRegressor(n_neighbors=5)
knn_copd.fit(Xcopd_train, ycopd_train)

# 5. printing results
print("\n" + "="*50)
print("PART 1: TOBACCO IMPACT ON CANCER")
print(f"Linear Regression R2: {lr_cancer.score(Xc_test, yc_test):.4f}")
print(f"KNN R2: {knn_cancer.score(Xc_test, yc_test):.4f}")
print("-" * 50)
print("PART 2: TOBACCO IMPACT ON COPD")
print(f"Linear Regression R2: {lr_copd.score(Xcopd_test, ycopd_test):.4f}")
print(f"KNN R2: {knn_copd.score(Xcopd_test, ycopd_test):.4f}")
print("="*50 + "\n")

# 6. visualizations (can make simpler if needed)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# Subplot 1: Cancer
ax1.scatter(final_table['Tobacco'], final_table['Cancer'], alpha=0.6, color='steelblue', label='State Data')
X_plot_c = final_table[['Tobacco']].sort_values(by='Tobacco')
ax1.plot(X_plot_c, lr_cancer.predict(scaler_c.transform(X_plot_c)), color='red', linewidth=2, label='Linear Trend')
ax1.set_title('Tobacco Use vs Cancer Prevalence')
ax1.set_xlabel('Tobacco Use (%)')
ax1.set_ylabel('Cancer Prevalence (%)')
ax1.legend()
ax1.grid(True, linestyle='--', alpha=0.3)

# Subplot 2: COPD
ax2.scatter(final_table['Tobacco'], final_table['Chronic Obstructive Pulmonary Disease'], alpha=0.6, color='darkorange', label='State Data')
X_plot_copd = final_table[['Tobacco']].sort_values(by='Tobacco')
ax2.plot(X_plot_copd, lr_copd.predict(scaler_copd.transform(X_plot_copd)), color='red', linewidth=2, label='Linear Trend')
ax2.set_title('Tobacco Use vs COPD Prevalence')
ax2.set_xlabel('Tobacco Use (%)')
ax2.set_ylabel('COPD Prevalence (%)')
ax2.legend()
ax2.grid(True, linestyle='--', alpha=0.3)

plt.tight_layout()
plt.show()