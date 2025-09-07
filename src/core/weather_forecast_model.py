from database import retrieve_data
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import numpy as np
import pandas as pd


def process_weather_dataset():
    df = retrieve_data()
    df["date"] = pd.to_datetime(df["date"])
    df["day_of_year"] = df["date"].dt.day_of_year
    df["month"] = df["date"].dt.month
    df["weekday"] = df["date"].dt.weekday

    df["prev_low_temp"] = df["lowest_temperature"].shift(1)
    df["prev_high_temp"] = df["highest_temperature"].shift(1)
    df["prev_second_low_temp"] = df["lowest_temperature"].shift(2)
    df["prev_second_high_temp"] = df["highest_temperature"].shift(2)
    df["prev_third_low_temp"] = df["lowest_temperature"].shift(3)
    df["prev_third_high_temp"] = df["highest_temperature"].shift(3)

    df["prev_low_temp"] = df["prev_low_temp"].fillna(df["lowest_temperature"].mean())
    df["prev_high_temp"] = df["prev_high_temp"].fillna(df["highest_temperature"].mean())

    df["low_3day_average"] = df["lowest_temperature"].rolling(3).mean().shift(1)
    df["high_3day_average"] = df["highest_temperature"].rolling(3).mean().shift(1)
    df["low_7day_average"] = df["lowest_temperature"].rolling(7).mean().shift(1)
    df["high_7day_average"] = df["highest_temperature"].rolling(7).mean().shift(1)
    df["low_14day_average"] = df["lowest_temperature"].rolling(14).mean().shift(1)
    df["high_14day_average"] = df["highest_temperature"].rolling(14).mean().shift(1)

    df["low_3day_average"] = df["low_3day_average"].fillna(
        df["lowest_temperature"].mean()
    )
    df["high_3day_average"] = df["high_3day_average"].fillna(
        df["highest_temperature"].mean()
    )

    df["low_14day_average"] = df["low_14day_average"].fillna(
        df["lowest_temperature"].mean()
    )
    df["high_14day_average"] = df["high_14day_average"].fillna(
        df["highest_temperature"].mean()
    )

    df["month_sin"] = np.sin(2 * np.pi * df["month"] / 12)
    df["month_cos"] = np.cos(2 * np.pi * df["month"] / 12)
    df["day_sin"] = np.sin(2 * np.pi * df["day_of_year"] / 365)
    df["day_cos"] = np.cos(2 * np.pi * df["day_of_year"] / 365)

    X = df[
        [
            "day_of_year",
            "weekday",
            "prev_low_temp",
            "prev_high_temp",
            "prev_second_low_temp",
            "prev_second_high_temp",
            "low_7day_average",
            "high_7day_average",
            "low_3day_average",
            "high_3day_average",
            "month_sin",
            "month_cos",
            "day_sin",
            "day_cos",
        ]
    ]
    y_low = df["lowest_temperature"]
    y_high = df["highest_temperature"]
    return X, y_low, y_high


def calculate_month_centers(month_days):
    centers = []
    for i in range(12):
        center = month_days[i] + month_days[i + 1] // 2
        centers.append(center)
    return centers



def prediction_plot(high_temp_predict, low_temp_predict):
    start_date = datetime.date(2025, 1, 1)
    end_date = datetime.date(2025, 12, 31)
    date_range = [start_date + datetime.timedelta(days=i) for i in range((end_date - start_date).days + 1)]

    high_temp_prediction = high_temp_predict[:len(date_range)]
    low_temp_prediction = low_temp_predict[:len(date_range)]

    _, ax = plt.subplots(figsize=(20, 5))
    ax.plot(date_range, high_temp_prediction, color="red", label="Prediction of high temperature")
    ax.plot(date_range, low_temp_prediction, color="blue", label="Prediction of low temperature")
    ax.fill_between(date_range, low_temp_prediction, high_temp_prediction, color="orange", alpha=0.2)
    ax.legend()

    
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))

    ax.set_xlabel("Month")
    ax.set_ylabel("Temperature")
    ax.set_title("Predicted High And Low Temperatures For All Days Of The Year of 2025")
    plt.tight_layout()
    plt.show()


def predict_temperature():
    X, y_low, y_high = process_weather_dataset()

    X_train, _, Y_low_train, _, Y_high_train, _ = train_test_split(
        X, y_low, y_high, test_size=0.2, shuffle=False
    )
    model_low = RandomForestRegressor(n_estimators=200, random_state=42)
    model_high = RandomForestRegressor(n_estimators=200, random_state=42)
    model_low.fit(X_train, Y_low_train)
    model_high.fit(X_train, Y_high_train)
    y_low_predict_all = model_low.predict(X)
    y_high_predict_all = model_high.predict(X)

    prediction_plot(y_high_predict_all, y_low_predict_all)
    print("Predicted lows for all days: ", y_low_predict_all)
    print("Predicted highs for all days: ", y_high_predict_all)

predict_temperature()
