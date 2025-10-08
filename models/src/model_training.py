from datetime import datetime
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.ensemble import RandomForestRegressor
from exploratory_data_analysis import data_cleaning_and_preprocessing
import pandas as pd

df = data_cleaning_and_preprocessing()


def get_date_parts(df):
    df["date"] = pd.to_datetime(df["date"])
    df["year"] = df["date"].dt.year
    df["day_of_year"] = df["date"].dt.dayofyear
    return df


def add_seasonality_feature(df):
    df["day_sin"] = np.sin(2 * np.pi * df["day_of_year"] / 365)
    df["day_cos"] = np.cos(2 * np.pi * df["day_of_year"] / 365)
    return df


def generate_features_for_training():
    global df
    X = df[["year", "day_of_year", "day_sin", "day_cos"]]
    y = df[["low_temperature", "high_temperature"]]
    return X, y


def training_and_testing_data(x, y):
    X_train, X_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=42
    )
    return X_train, X_test, y_train, y_test


def get_current_date():
    today = pd.to_datetime(datetime.today().strftime("%Y-%m-%d"))
    year = today.year
    day = today.day_of_year
    day_sin_value = np.sin(2 * np.pi * day / 365)
    day_cos_value = np.cos(2 * np.pi * day / 365)
    X_test_today = pd.DataFrame(
        {
            "year": [year],
            "day_of_year": [day],
            "day_sin": [day_sin_value],
            "day_cos": [day_cos_value],
        }
    )
    return X_test_today


def model_tuning_for_linear_regression():
    global df
    df = get_date_parts(df)
    df = add_seasonality_feature(df)
    X, y = generate_features_for_training()
    param_space = {
        "copy_X": [True, False],
        "fit_intercept": [True, False],
        "n_jobs": [1, 5, 10, 15, None],
        "positive": [True, False],
    }
    X_train, _, y_train, _ = training_and_testing_data(X, y)
    model = LinearRegression()
    random_search = RandomizedSearchCV(model, param_space, cv=5)
    random_search.fit(X_train, y_train)
    return random_search.best_estimator_, random_search.best_params_


def model_tuning_for_random_forest_regressor():
    global df
    df = get_date_parts(df)
    df = add_seasonality_feature(df)
    X, y = generate_features_for_training()
    param_grid = {
        "n_estimators": [100, 200, 500, 1000],
        "max_depth": [None, 10, 20, 30],
        "min_samples_split": [2, 5, 10],
        "min_samples_leaf": [1, 2, 4],
        "bootstrap": [True, False],
    }
    X_train, _, y_train, _ = training_and_testing_data(X, y)
    model = RandomForestRegressor(max_depth=3, n_estimators=50)
    random_search = RandomizedSearchCV(
        model, param_grid, cv=5, n_iter=5, n_jobs=1, random_state=42
    )
    random_search.fit(X_train, y_train)
    return random_search.best_estimator_, random_search.best_params_


def model_training_based_on_linear_regression():
    global df
    df = get_date_parts(df)
    df = add_seasonality_feature(df)
    X, y = generate_features_for_training()
    X_train, _, y_train, _ = training_and_testing_data(X, y)
    model = LinearRegression(n_jobs=5, copy_X=True, fit_intercept=True, positive=False)
    model.fit(X_train, y_train)
    predict = model.predict(get_current_date())
    return f"low temperature: {predict[0][0]}, high temperature: {predict[0][1]}"


def model_training_based_on_random_forest_regressor():
    global df
    df = get_date_parts(df)
    df = add_seasonality_feature(df)
    X, y = generate_features_for_training()
    X_train, _, y_train, _ = training_and_testing_data(X, y)
    model = RandomForestRegressor(
        bootstrap=True,
        max_depth=10,
        max_leaf_nodes=5,
        min_samples_leaf=1,
        min_samples_split=5,
        n_estimators=500,
    )
    model.fit(X_train, y_train)
    predict = model.predict(get_current_date())
    return f"low temperature: {predict[0][0]}, high temperature: {predict[0][1]}"
