import sqlite3
import sys
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
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
    df["date"] = pd.to_datetime(df["date"]).dt.date
    daily_mean = round(
        df.groupby(df["date"]).agg(
            low_temperature=("low_temperature", "mean"),
            high_temperature=("high_temperature", "mean"),
        )
    ).reset_index()
    return daily_mean


def check_for_outliers_in_temperatures_per_month(df, column):
    df["month"] = pd.to_datetime(df["date"]).dt.month
    for month in range(1, 13):
        temperature_per_month = df[df["month"] == month][column]
        Q1 = temperature_per_month.quantile(0.25)
        Q3 = temperature_per_month.quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        outliers = temperature_per_month[
            (temperature_per_month < lower_bound)
            | (temperature_per_month > upper_bound)
        ]
        return outliers


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
    df = calculate_average_low_and_high_temperature_per_day(df)
    return df
