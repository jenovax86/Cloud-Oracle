import sqlite3
import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../../crawler/src/"))
)
database_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../weather_forecast")
)
sys.path.append(database_path)
from database.db import get_weather_records
from utils import remove_temperature_signs

sqlite_connection = sqlite3.connect(database_path)


def convert_temperatures_to_integer(df):
    df["low_temperature"] = pd.to_numeric(
        remove_temperature_signs(df["low_temperature"]), errors="coerce"
    )
    df["high_temperature"] = pd.to_numeric(
        remove_temperature_signs(df["high_temperature"])
    )
    return df


def calculate_average_low_and_high_temperature_per_day(df):
    df["date"] = pd.to_datetime(df["date"])
    df["date"] = df["date"].dt.date
    round(df.groupby(df["date"])[["low_temperature", "high_temperature"]].mean())
    return df

def check_for_outliers_in_temperatures_per_month(df, column):
    for month in range(1, 13):
        temp_per_month = df[df["month"] == month][column]
        Q1 = temp_per_month.quantile(0.25)
        Q3 = temp_per_month.quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 - 1.5 * IQR
        outliers = temp_per_month[
            (df[column] < lower_bound) | (df[column] > upper_bound)
        ]
        print(f"Month {month}")
        print("Lower bound:", lower_bound)
        print("Upper bound:", upper_bound)
        print("Outliers found:", len(outliers))
        print("Sample outliers:\n", outliers.head(), "\n")


def scatter_plot_of_temperatures(df):
    plt.title("Scatter plot for temperatures")
    sns.scatterplot(x=df["low_temperature"], y=df["high_temperature"])
    plt.show()


def plot_time_series(df):
    plt.figure(figsize=(12, 6))
    plt.plot(df["date"], df["low_temperature"])
    plt.plot(df["date"], df["high_temperature"])
    plt.legend()
    plt.title("Plot for low temperatures over time")
    plt.xlabel("date")
    plt.ylabel("temperatures")
    plt.show()


def data_cleaning_and_preprocessing():
    weather_data = get_weather_records(sqlite_connection)
    df = pd.DataFrame(weather_data)
    df.columns = ["id", "date", "low_temperature", "high_temperature"]
    df.dropna(inplace=True)
    df.drop_duplicates(inplace=True)
    df = convert_temperatures_to_integer(df)
    check_for_outliers_in_temperatures_per_month(df, "low_temperature")
    check_for_outliers_in_temperatures_per_month(df, "high_temperature")
    calculate_average_low_and_high_temperature_per_day(df)
    print(df.head())
    return df


data_cleaning_and_preprocessing()
