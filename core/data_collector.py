from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from calendar import monthrange
import pandas as pd
import time
import os

MONTHS = {
    "january": 1,
    "february": 2,
    "march": 3,
    "april": 4,
    "may": 5,
    "june": 6,
    "july": 7,
    "august": 8,
    "september": 9,
    "october": 10,
    "november": 11,
    "december": 12,
}
COUNTRY = "iran"
YEAR = 2024


def extract_month_days(days, month_number):
    valid_days = []
    _, num_of_days = monthrange(YEAR, month_number)
    for day in days:
        date_value = day.find_element(By.CLASS_NAME, "date").text.strip()
        if not date_value.isdigit():
            continue

        date_number = int(date_value)
        if 1 <= date_number <= num_of_days:
            date = datetime(YEAR, month_number, date_number)
            valid_days.append((date, day))

    return valid_days


def parse_daily_temperatures(month_days, month_name):
    weather_data = []
    for date_num, day in month_days:
        temp_parent_element = day.find_element(By.CLASS_NAME, "temp")
        temp_low = (
            temp_parent_element.find_element(By.CLASS_NAME, "low").text
            if temp_parent_element.find_element(By.CLASS_NAME, "low")
            else None
        )
        temp_high = (
            temp_parent_element.find_element(By.CLASS_NAME, "high").text
            if temp_parent_element.find_element(By.CLASS_NAME, "high")
            else None
        )
        weather_data.append(
            {
                "month": month_name,
                "day": date_num.strftime("%a"),
                "date": date_num.strftime("%Y-%m-%d"),
                "lowest_temperature": temp_low,
                "highest_temperature": temp_high,
            }
        )

    return weather_data


def data_preprocessing(df):
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.drop_duplicates(subset=["date"], keep="first").reset_index(drop=True)
    df = df.sort_values("date").reset_index(drop=True)

    for column in ["lowest_temperature", "highest_temperature"]:
        df[column] = df[column].astype(str).str.replace(r"[^0-9\-]", "", regex=True)
        df[column] = pd.to_numeric(df[column], errors="coerce").astype("Int64")

    df = df.dropna(subset=["lowest_temperature", "highest_temperature"])
    return df


def scrape_weather_data():
    weather_scrapped_data = []
    driver = webdriver.Chrome()
    for month_name, month_number in MONTHS.items():
        url = f"https://www.accuweather.com/en/ru/{COUNTRY}/605458/{month_name}-weather/605458?year=2024"
        driver.get(url)
        time.sleep(2)

        days = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".monthly-daypanel"))
        )
        month_days = extract_month_days(days, month_number)
        result = parse_daily_temperatures(month_days, month_name)
        weather_scrapped_data.extend(result)

    driver.quit()
    df = pd.DataFrame(weather_scrapped_data)
    return clean_data(df)


def main():
    current_dir = os.getcwd()
    parent_dir = os.path.dirname(current_dir)
    new_folder = os.path.join(parent_dir, "data")

    try:
        os.makedirs(new_folder)
    except FileExistsError:
        print("Directory already exists.")

    data = scrape_weather_data()
    data.to_csv("../data/weather_data.csv")

main()