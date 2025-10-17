from datetime import datetime
import joblib

from utils import date_to_data_frame


linear_regression_model = joblib.load("linear_regression.joblib")
random_forest_regressor_model = joblib.load("random_forest_regressor.joblib")
today = date_to_data_frame(datetime.today().strftime("%Y-%m-%d %H"))
predict_result_of_linear_regression_model = linear_regression_model.predict(today)
print(
    f"linear regression low temperature: {round(predict_result_of_linear_regression_model[0][0])}, high temperature: {round(predict_result_of_linear_regression_model[0][1])}"
)
predict_result_of_random_forest_regressor_model = random_forest_regressor_model.predict(
    today
)
print(
    f"random forest low temperature: {round(predict_result_of_random_forest_regressor_model[0][0])}, high temperature: {round(predict_result_of_random_forest_regressor_model[0][1])}"
)
