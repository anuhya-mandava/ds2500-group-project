"""
Anuhya Mandava
DS2500
Final Project
FinalProject.py
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

BASE_PATH = "C:\\Users\\anuhy\\DS2500\\FinalProject\\"
df = pd.read_csv(BASE_PATH + "U.S._Chronic_Disease_Indicators (1).csv")


def save_results(disease, filename):
    """
    Save cleaned data for a disease topic to a new CSV file.

    Parameters: str, disease, topic name to filter by
                str, filename, name of output CSV file

    Returns: None
    """
    cleaned_data = df.dropna(axis=1, how='all')
    disease_rows = cleaned_data[cleaned_data["Topic"] == disease]
    disease_rows.to_csv(BASE_PATH + filename, index=False)
    print(f"Results saved to {filename} for {disease}")


def filter_data(dataframe, year):
    """
    Filter data to a specific year, US level, and Overall stratification.

    Parameters: dataframe, dataframe, disease dataframe
                int, year, year to filter by

    Returns: dataframe, filtered dataframe
    """
    filtered = dataframe[
        (dataframe["YearStart"] == year) &
        (dataframe["LocationDesc"] == "United States") &
        (dataframe["Stratification1"] == "Overall")
    ].copy()
    return filtered


def normalize_rate(value, value_type):
    """
    Normalize a single rate value to 0-1 based on its DataValueType.
    - Percentage -> divide by 100
    - Per 100,000 -> divide by 100,000
    - Per 1,000 -> divide by 1,000
    - Unknown -> return None

    Parameters: float, value, the raw data value
                str, value_type, the DataValueType string

    Returns: float or None, normalized value
    """
    dtype = str(value_type).lower()

    if "%" in dtype or "percent" in dtype:
        return value / 100
    elif "100,000" in dtype:
        return value / 100000
    elif "1,000" in dtype:
        return value / 1000
    else:
        return None


def get_indicator_rates(dataframe):
    """
    For each indicator (Question), compute the normalized rate.

    Parameters: dataframe, dataframe, filtered disease dataframe

    Returns: dataframe, result, with columns Question and NormalizedRate
    """
    rows = []
    for _, row in dataframe.iterrows():
        normalized = normalize_rate(row["DataValue"], row["DataValueType"])
        if normalized is not None:
            rows.append({
                "Question": row["Question"],
                "DataValueType": row["DataValueType"],
                "RawRate": row["DataValue"],
                "NormalizedRate": normalized
            })

    result = pd.DataFrame(rows).dropna(subset=["NormalizedRate"])
    return result


def plot_indicator_rates(indicator_df, topic, year):
    """
    Plot a bar chart of normalized rates for each indicator in a topic.

    Parameters: dataframe, indicator_df, dataframe with Question and NormalizedRate columns
                str, topic, topic name for the title
                int, year, year for the title

    Returns: None
    """
    plt.figure(figsize=(12, 6))
    sns.barplot(data=indicator_df, x="NormalizedRate", y="Question", palette="Blues_d")
    plt.xlabel("Normalized Rate (0-1)")
    plt.ylabel("Indicator")
    plt.title(f"{topic} Indicator Rates - {year} (US Overall)")
    plt.tight_layout()
    plt.savefig(BASE_PATH + f"{topic.replace(' ', '_')}_{year}_indicators.png")
    plt.show()
    print(f"Plot saved for {topic} {year}")


def main():
    # save disease-specific CSVs
    save_results("Mental Health", "mental_health_data.csv")
    save_results("Alcohol", "alcohol_data.csv")

    mental_health_df = pd.read_csv(BASE_PATH + "mental_health_data.csv")
    alcohol_df = pd.read_csv(BASE_PATH + "alcohol_data.csv")

    # print available years and questions
    print("Mental Health years:", sorted(mental_health_df["YearStart"].unique()))
    print("Alcohol years:", sorted(alcohol_df["YearStart"].unique()))

    # user picks a year
    year = int(input("Enter a year to analyze: "))

    # filter to US overall for selected year
    mental_filtered = filter_data(mental_health_df, year)
    alcohol_filtered = filter_data(alcohol_df, year)

    # get normalized rates per indicator
    mental_rates = get_indicator_rates(mental_filtered)
    alcohol_rates = get_indicator_rates(alcohol_filtered)

    print("\nMental Health Indicators:")
    print(mental_rates)
    print("\nAlcohol Indicators:")
    print(alcohol_rates)

    # plot indicator rates
    plot_indicator_rates(mental_rates, "Mental Health", year)
    plot_indicator_rates(alcohol_rates, "Alcohol", year)


if __name__ == "__main__":
    main()