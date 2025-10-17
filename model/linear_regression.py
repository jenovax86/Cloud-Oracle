from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

from utils import cyclical_feature_encoding


def train(df):
    df["day_sin"], df["day_cos"] = cyclical_feature_encoding(df["day_of_year"])
    df["month_sin"], df["month_cos"] = cyclical_feature_encoding(df["month"])
    x = df[
        [
            "year",
            "month",
            "month_sin",
            "month_cos",
            "day_of_year",
            "day_sin",
            "day_cos",
            "hour_of_day"
        ]
    ]
    y = df[["low_temperature", "high_temperature"]]
    x_train, _, y_train, _ = train_test_split(x, y, test_size=0.2, random_state=42)
    model = LinearRegression(n_jobs=5, copy_X=True, fit_intercept=True, positive=False)
    model.fit(x_train, y_train)
    return model
