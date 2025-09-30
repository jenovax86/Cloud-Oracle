from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from bs4 import BeautifulSoup
from database.db import insert_weather_records, get_weather_records, find_last_year

WEBDRIVER_TIMEOUT = 20


def temperature_remove_signs(temperature):
    return int(temperature.split(":")[1])


def generate_date(year, month, days_of_month, time):
    date_string = f"{year}-{month}-{days_of_month} {time}"
    return datetime.strptime(date_string, "%Y-%m-%d %H:%M")


def parse_daily_weather_summary(driver, year, month):
    weather_data_summary = []
    days_of_month = 0
    try:
        WebDriverWait(driver, WEBDRIVER_TIMEOUT).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[@id = 'weather']"))
        )
        weather_container = driver.find_element(
            By.XPATH, "//div[@id = 'weather']"
        ).get_attribute("outerHTML")
        soup = BeautifulSoup(weather_container, "html.parser")
        sections = soup.select("div[id^=ws_]")
        for section in sections:
            date_div = section.find("div", class_="date")
            if date_div:
                days_of_month += 1

            time = (
                section.find("div", class_="time").get_text(strip=True)
                if section.find("div", class_="time")
                else ""
            )
            low_temperature = (
                section.find("div", class_="tempLow low").get_text(strip=True)
                if section.find("div", class_="tempLow low")
                else ""
            )
            high_temperature = (
                section.find("div", class_="temp low").get_text(strip=True)
                if section.find("div", class_="temp low")
                else ""
            )
            weather_data_summary.append(
                {
                    "date": generate_date(year, month, days_of_month, time),
                    "low_temperature": low_temperature,
                    "high_temperature": high_temperature,
                }
            )

        return weather_data_summary

    except StaleElementReferenceException as error:
        raise ValueError(error)


def crawl_weather_data():
    driver = webdriver.Chrome()
    past_year = int(datetime.now().year - 1)
    last_available_year = 2010 - 1
    last_month_of_the_year = 12 + 1
    descending_order = -1
    last_available_year_in_database = find_last_year()
    if not last_available_year_in_database or last_available_year_in_database[0][0] is None:
        for year in range(past_year, last_available_year, descending_order):
            for month in range(1, last_month_of_the_year):
                driver.get(
                    f"https://www.timeanddate.com/weather/iran/tehran/historic?month={month}&year={year}"
                )
                weather_data = parse_daily_weather_summary(driver, year, month)
                insert_weather_records(weather_data)
        driver.quit()
        print(get_weather_records())


crawl_weather_data()
