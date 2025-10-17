import numpy as np
import pandas as pd


def cyclical_feature_encoding(day):
    return np.sin(2 * np.pi * day / 365), np.cos(2 * np.pi * day / 365)


def date_to_data_frame(date):
    df = pd.to_datetime(date)
    day_sin, day_cos = cyclical_feature_encoding(df.day_of_year)
    month_sin, month_cos = cyclical_feature_encoding(df.month)
    return pd.DataFrame(
        {
            "year": [df.year],
            "month": [df.month],
            "month_sin": [month_sin],
            "month_cos": [month_cos],
            "day_of_year": [df.day_of_year],
            "day_sin": [day_sin],
            "day_cos": [day_cos],
            "hour_of_day": [df.hour],
        }
    )
