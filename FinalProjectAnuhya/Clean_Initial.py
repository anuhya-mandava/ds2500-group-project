import pandas as pd
import numpy as np
import seaborn as sns
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

df = pd.read_csv(r"FinalProject\U.S._Chronic_Disease_Indicators (1).csv")

def save_results(disease, filename):
    """
    Save cleaned data for disease to a new CSV file.

    Parameters: str, disease 
                str, filename

    Returns: None
    """
    cleaned_data = df.dropna(axis=1, how='all')
    """cleaned_data = cleaned_data.drop(columns=[
        "Geolocation", "LocationID", "TopicID", "QuestionID",
        "DataValueTypeID", "StratificationCategoryID1", "StratificationID1"])"""
    disease_rows = cleaned_data[cleaned_data["Topic"] == disease]
    disease_rows.to_csv("C:\\Users\\anuhy\\DS2500\\FinalProject\\" + filename, index=False)
    print(f"Results saved to {filename} for {disease}")


def perform_kmeans(x, n_clusters):
    """
    Performs K-means clustering on the given data.

    Parameters: list of lists, x, feature data
                int, n_clusters, number of clusters to form

    Returns: list, kmean_cluster_labels, the cluster label for data sublist
    """
    kmeans = sklearn.cluster.KMeans(n_clusters=n_clusters, random_state=2500)
    kmeans.fit(x)
    kmean_cluster_labels = kmeans.labels_.tolist()
    return kmean_cluster_labels

# PROBLEM 02
def perform_hierarchical(x, n_clusters):
    """
    Performs hierarchical clustering on the given data.

    Parameters: list of lists, x, feature data
                int, n_clusters, number of clusters to form

    Returns: list, hierarchical_cluster_labels, the cluster label for data sublist
    """
    hierarchical = sklearn.cluster.AgglomerativeClustering(n_clusters=n_clusters, linkage="average")
    hierarchical.fit(x)
    hierarchical_cluster_labels = hierarchical.labels_.tolist()
    return hierarchical_cluster_labels

def find_optimal_clusters(x, clustering_option="kmeans", max_k=10):
    """
    Determines optimal number of clusters

    Parameters: list of lists, x, feature data
                str, clustering_option, either "kmeans" or "hierarchical"
                max_k, n_clusters, number of clusters to form

    Returns: float, best_k, optimal cluster number
    """
    best_k = 1
    best_score = -10

    for k in range(2, max_k + 1):
        if clustering_option == "kmeans":
            cluster_labels = perform_kmeans(x, n_clusters=k)
        elif clustering_option == "hierarchical":
            cluster_labels = perform_hierarchical(x, n_clusters=k)
        else:
            raise ValueError("Invalid clustering option. Choose 'kmeans' or 'hierarchical'.")

        score = sklearn.metrics.silhouette_score(x, cluster_labels)
        score = float(score)
        print(f"Silhouette Score: {score:.3f}")

        if score > best_score:
            best_score = score
            best_k = k

    return best_k

def save_clustering_results(labels, filename):
    """
    Saves the cluster labels to a CSV file.

    Parameters: list, labels, predicted cluster labels
                str, filename, name of the output CSV file

    Returns: none
    """
    with open(filename, mode='w', newline='') as file:
        file.write("cluster_label\n")
        for label in labels:
            file.write(str(label) + "\n")

def split_data(df):
    """
    Split the data into training, validation, and test sets.

    Parameters:  dataframe, df

    Return: df, training_features
            df, validation_features
            df, test_features
            series, training_labels
            series, validation_labels
            series, test_labels
    """
    x = df.drop(columns=['Stress_level'])
    y = df['Stress_level']

    temp_features, test_features, temp_labels, test_labels = train_test_split(x, y, test_size=0.2, train_size=0.8, random_state=2500)
    training_features, validation_features, training_labels, validation_labels = train_test_split(temp_features, temp_labels, test_size=0.2, train_size=0.8, random_state=2500)

    return training_features, validation_features, test_features, training_labels, validation_labels, test_labels

# PROBLEM 02
def feature_selection(training_features, validation_features, test_features, selected_features):
    """
    Select specific features from the datasets.

    Parameters:  df, training_features
                 df, validation_features
                 df, test_features
                 list, selected_features

    Return: df, selected_training_features
            df, selected_validation_features
            df, selected_test_features
    """
    training_features_selected = training_features[selected_features]
    validation_features_selected = validation_features[selected_features]
    test_features_selected = test_features[selected_features]

    return training_features_selected, validation_features_selected, test_features_selected

# PROBLEM 03
def train_model(training_features, training_labels):
    """
    Train a linear regression model using the training data.

    Parameters:  df, training_features
                 series, training_labels

    Return: model, trained linear regression model
    """
    model = LinearRegression()
    model.fit(training_features, training_labels)
    return model

# PROBLEM 04
def evaluate_model(model, features, labels):
    """
    Evaluate the model using Mean Squared Error (MSE).

    Parameters:  model, trained linear regression model
                 df, features
                 series, labels

    Return: float, mean squared error
    """
    predictions = model.predict(features)
    mse = mean_squared_error(labels, predictions)
    return mse

def state_correlations(year, dataframe):
    """
    Calculate the state correlations
    """

def main():
    save_results("Mental Health", "mental_health_data.csv")
    save_results("Alcohol", "alcohol_data.csv")

    mental_health_df = pd.read_csv(r"FinalProject\mental_health_data.csv")
    alcohol_df = pd.read_csv(r"FinalProject\alcohol_data.csv")
    print(mental_health_df.size)
    print(alcohol_df.size)

    #print(mental_health_df["Question"].unique())
    #print("-----------------------------")
    #print(alcohol_df["Question"].unique())

if __name__ == "__main__":
    main()


