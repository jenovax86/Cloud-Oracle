from sklearn.ensemble import RandomForestRegressor
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
            "hour_of_day",
        ]
    ]
    y = df[["low_temperature", "high_temperature"]]
    x_train, _, y_train, _ = train_test_split(x, y, test_size=0.2, random_state=42)
    model = RandomForestRegressor(
        bootstrap=False,
        max_depth=30,
        max_leaf_nodes=5,
        min_samples_leaf=1,
        min_samples_split=5,
        n_estimators=100,
    )
    model.fit(x_train, y_train)
    return model
