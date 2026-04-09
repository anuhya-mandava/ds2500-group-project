"""
DS 2500 cd ~/Desktop
Min Yu Huang: Diabetes & Obesity Analysis
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import LeaveOneOut
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
import plotly.express as px


# 1. LOAD & BUILD STATE-LEVEL DATASET (2022)
df = pd.read_csv("cleaned_diabetes_obesity_indicators.csv")

def get_indicator(question, year=2022, strat="Overall", val_type="Age-adjusted Prevalence"):
    subset = df[
        (df["Question"] == question) &
        (df["StratificationCategory1"] == strat) &
        (df["DataValueType"] == val_type) &
        (df["YearStart"] == year)
    ][["LocationAbbr", "LocationDesc", "DataValue"]]
    return subset.dropna()

diabetes = get_indicator("Diabetes among adults").rename(
    columns={"DataValue": "diabetes_prevalence", "LocationDesc": "State"})

obesity = get_indicator("Obesity among adults").rename(
    columns={"DataValue": "obesity_rate"})

# Merge
state_df = diabetes.merge(obesity[["LocationAbbr", "obesity_rate"]], on="LocationAbbr")
print(f"Dataset: {state_df.shape[0]} states/territories")
print(state_df.describe())


# 2. EDA: Correlation & Scatter Plot
r, p = stats.pearsonr(state_df["obesity_rate"], state_df["diabetes_prevalence"])
print(f"\nPearson r (obesity vs diabetes): {r:.3f}, p-value: {p:.4f}")

plt.figure(figsize=(8, 5))
plt.scatter(state_df["obesity_rate"], state_df["diabetes_prevalence"],
            color="steelblue", alpha=0.7, edgecolors="white")

# Regression line
m, b = np.polyfit(state_df["obesity_rate"], state_df["diabetes_prevalence"], 1)
x_line = np.linspace(state_df["obesity_rate"].min(), state_df["obesity_rate"].max(), 100)
plt.plot(x_line, m * x_line + b, color="tomato", linewidth=2)

# Label notable states
for _, row in state_df.iterrows():
    if row["diabetes_prevalence"] > 13 or row["diabetes_prevalence"] < 8:
        plt.annotate(row["LocationAbbr"],
                     (row["obesity_rate"], row["diabetes_prevalence"]),
                     textcoords="offset points", xytext=(5, 3), fontsize=7)

plt.xlabel("Obesity Rate (%)")
plt.ylabel("Diabetes Prevalence (%)")
plt.title(f"Obesity vs Diabetes Prevalence by State (2022)\nPearson r = {r:.3f}, p = {p:.4f}")
plt.tight_layout()
plt.savefig("scatter_obesity_diabetes.png", dpi=150)
plt.show()
print("Scatter plot saved.")


# 3. MODELS-LOOCV
X_raw = state_df[["obesity_rate"]].values
y = state_df["diabetes_prevalence"].values

scaler = StandardScaler()
X = scaler.fit_transform(X_raw)

loo = LeaveOneOut()

# Linear Regression
lr = LinearRegression()
lr_preds, lr_actuals = [], []
for train_idx, test_idx in loo.split(X):
    lr.fit(X[train_idx], y[train_idx])
    lr_preds.append(lr.predict(X[test_idx])[0])
    lr_actuals.append(y[test_idx][0])

lr_r2   = r2_score(lr_actuals, lr_preds)
lr_rmse = np.sqrt(mean_squared_error(lr_actuals, lr_preds))
print(f"\nLinear Regression (LOOCV) — R²: {lr_r2:.3f}, RMSE: {lr_rmse:.3f}")

# KNN Regression (try k = 3, 5, 7, 9)
print("\nKNN Results:")
best_k, best_r2, best_rmse = None, -np.inf, None
for k in [3, 5, 7, 9]:
    knn_preds = []
    for train_idx, test_idx in loo.split(X):
        knn = KNeighborsRegressor(n_neighbors=k)
        knn.fit(X[train_idx], y[train_idx])
        knn_preds.append(knn.predict(X[test_idx])[0])
    r2_k   = r2_score(lr_actuals, knn_preds)
    rmse_k = np.sqrt(mean_squared_error(lr_actuals, knn_preds))
    print(f"  k={k}: R²={r2_k:.3f}, RMSE={rmse_k:.3f}")
    if r2_k > best_r2:
        best_k, best_r2, best_rmse = k, r2_k, rmse_k

print(f"\nBest KNN: k={best_k}, R²={best_r2:.3f}, RMSE={best_rmse:.3f}")


# 4. CHOROPLETH MAP—Diabetes Prevalence
fig_diabetes = px.choropleth(
    state_df,
    locations="LocationAbbr",
    locationmode="USA-states",
    color="diabetes_prevalence",
    scope="usa",
    color_continuous_scale="Reds",
    title="Diabetes Prevalence by State (2022, Age-adjusted %)",
    labels={"diabetes_prevalence": "Diabetes (%)"}
)
fig_diabetes.write_html("choropleth_diabetes.html")
fig_diabetes.show()

fig_obesity = px.choropleth(
    state_df,
    locations="LocationAbbr",
    locationmode="USA-states",
    color="obesity_rate",
    scope="usa",
    color_continuous_scale="Oranges",
    title="Obesity Rate by State (2022, Age-adjusted %)",
    labels={"obesity_rate": "Obesity (%)"}
)
fig_obesity.write_html("choropleth_obesity.html")
fig_obesity.show()

print("\nChoropleth maps saved as HTML.")

# 5. TOP/BOTTOM STATES SUMMARY
print("\n--- Top 5 highest diabetes prevalence ---")
print(state_df.nlargest(5, "diabetes_prevalence")[
    ["State", "LocationAbbr", "diabetes_prevalence", "obesity_rate"]].to_string(index=False))

print("\n--- Top 5 lowest diabetes prevalence ---")
print(state_df.nsmallest(5, "diabetes_prevalence")[
    ["State", "LocationAbbr", "diabetes_prevalence", "obesity_rate"]].to_string(index=False))