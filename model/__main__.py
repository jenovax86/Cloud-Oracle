import joblib
import sqlite3
import model.linear_regression
import model.random_forest_regressor
from model.preprocess import preprocess_data
from database.db import get_weather_records
from constants import DATABASE_PATH


def main():
    sqlite_connection = sqlite3.connect(DATABASE_PATH)
    weather_data = get_weather_records(sqlite_connection)
    df = preprocess_data(weather_data)
    linear_regression_model = model.linear_regression.train(df)
    random_forest_regressor_model = model.random_forest_regressor.train(df)
    joblib.dump(linear_regression_model, "./linear_regression.joblib")
    joblib.dump(random_forest_regressor_model, "./random_forest_regressor.joblib")


if __name__ == "__main__":
    main()
