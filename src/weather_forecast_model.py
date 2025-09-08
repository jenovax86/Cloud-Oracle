from db import get_weather_records, connect
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import numpy as np
import pandas as pd


def process_weather_dataset(df):
    print(df)


process_weather_dataset()


def prediction_plot(high_temp_predict, low_temp_predict):
    start_date = datetime.date(2025, 1, 1)
    end_date = datetime.date(2025, 12, 31)
    date_range = [
        start_date + datetime.timedelta(days=i)
        for i in range((end_date - start_date).days + 1)
    ]

    high_temp_prediction = high_temp_predict[: len(date_range)]
    low_temp_prediction = low_temp_predict[: len(date_range)]

    _, ax = plt.subplots(figsize=(20, 5))
    ax.plot(
        date_range,
        high_temp_prediction,
        color="red",
        label="Prediction of high temperature",
    )
    ax.plot(
        date_range,
        low_temp_prediction,
        color="blue",
        label="Prediction of low temperature",
    )
    ax.fill_between(
        date_range, low_temp_prediction, high_temp_prediction, color="orange", alpha=0.2
    )
    ax.legend()

    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))

    ax.set_xlabel("Month")
    ax.set_ylabel("Temperature")
    ax.set_title("Predicted High And Low Temperatures For All Days Of The Year of 2025")
    plt.tight_layout()
    plt.show()


def predict_temperature(data_frame):
    X, y_low, y_high = process_weather_dataset(data_frame)

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
