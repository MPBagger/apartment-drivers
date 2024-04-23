import mlflow

import pandas as pd
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import mean_squared_error


def split_data(df, target_column, test_size=0.2, random_state=42):
    X = df.drop(target_column, axis=1)
    y = df[target_column]
    return X, y


def train_linear_regression(df,
                              target_column = "price",
                              test_size=0.2, 
                              random_state=42
                              ):

    # Split the data
    X, y = split_data(df, target_column=target_column)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)

    # One-Hot Encoding:
    encoder_one_hot = OneHotEncoder()
    X_train_one_hot = encoder_one_hot.fit_transform(X_train[['energy_l', 'varme', 'roof_type']])

    # Build linear regression model
    model_one_hot = LinearRegression()
    model_one_hot.fit(X_train_one_hot, y_train)

    # Evaluate model on the test set
    X_test_one_hot = encoder_one_hot.transform(X_test[['energy_l','varme', 'roof_type']])
    y_pred_one_hot = model_one_hot.predict(X_test_one_hot)
    mse = mean_squared_error(y_test, y_pred_one_hot)        

    # # Set our tracking server uri for logging
    # mlflow.set_tracking_uri(uri="http://127.0.0.1:8080/")

    # Create a new MLflow Experiment
    mlflow.set_experiment("MLflow Apartment Price Model")

    # Start an MLflow run
    with mlflow.start_run():

        # Log the loss metric
        mlflow.log_metric("mse", mse)

        # Set a tag that we can use to remind ourselves what this run was for
        mlflow.set_tag("Training Info", "Basic linear regression model for the apartment price dataset.")

        # Log the model
        model_info = mlflow.sklearn.log_model(
            sk_model=model_one_hot,
            artifact_path="apartment_price_model",
            input_example=X_train,
            registered_model_name="linear_regression_model",
        )
