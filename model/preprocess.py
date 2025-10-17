import pandas as pd

from model.utils import remove_temperature_sign


def preprocess_data(weather_data):
    df = pd.DataFrame(weather_data)
    df.columns = ["id", "date", "low_temperature", "high_temperature"]
    df.dropna(inplace=True)
    df.drop_duplicates(inplace=True)
    df["low_temperature"] = pd.to_numeric(
        remove_temperature_sign(df["low_temperature"]), errors="coerce"
    )
    df["high_temperature"] = pd.to_numeric(
        remove_temperature_sign(df["high_temperature"])
    )
    df["date"] = pd.to_datetime(df["date"])
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    df["day_of_year"] = df["date"].dt.dayofyear
    df["hour_of_day"] = df["date"].dt.hour
    return df
