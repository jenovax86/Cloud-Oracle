import sqlite3
import sys
import os
import pandas as pd

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../../crawler/src/"))
)
database_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../weather_forecast")
)
sys.path.append(database_path)
from database.db import get_weather_records
from utils import remove_temperature_signs


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


def data_cleaning_and_preprocessing():
    sqlite_connection = sqlite3.connect(database_path)
    weather_data = get_weather_records(sqlite_connection)
    df = pd.DataFrame(weather_data)
    df.columns = ["id", "date", "low_temperature", "high_temperature"]
    df.dropna(inplace=True)
    df.drop_duplicates(inplace=True)
    df = convert_temperatures_to_integer(df)
    df = calculate_average_low_and_high_temperature_per_day(df)
    return df
