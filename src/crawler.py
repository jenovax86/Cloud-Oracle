from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from bs4 import BeautifulSoup
from database.db import insert_weather_records, find_last_year

WEBDRIVER_TIMEOUT = 20
PAST_YEAR = int(datetime.now().year - 1)
LAST_AVAILABLE_YEAR = 2010 - 1
FIRST_MONTH_OF_YEAR = 1
LAST_MONTH_OF_YEAR = 12 + 1
DESCENDING_ORDER = -1


def generate_datetime(year, month, days_of_month, time):
    date_string = f"{year}-{month}-{days_of_month} {time}"
    return datetime.strptime(date_string, "%Y-%m-%d %H:%M")


def parse_daily_weather_data(driver, year, month):
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
                else None
            )
            low_temperature = (
                section.find("div", class_="tempLow low").get_text(strip=True)
                if section.find("div", class_="tempLow low")
                else None
            )
            high_temperature = (
                section.find("div", class_="temp low").get_text(strip=True)
                if section.find("div", class_="temp low")
                else None
            )
            weather_data_summary.append(
                {
                    "date": generate_datetime(year, month, days_of_month, time),
                    "low_temperature": low_temperature,
                    "high_temperature": high_temperature,
                }
            )

        return weather_data_summary

    except StaleElementReferenceException as error:
        raise ValueError(error)


def scrape_weather_data(driver, end_year):
    for year in range(PAST_YEAR, end_year, DESCENDING_ORDER):
        for month in range(FIRST_MONTH_OF_YEAR, LAST_MONTH_OF_YEAR):
            driver.get(
                f"https://www.timeanddate.com/weather/iran/tehran/historic?month={month}&year={year}"
            )
            weather_data = parse_daily_weather_data(driver, year, month)
            insert_weather_records(weather_data)


def run_weather_crawler():
    driver = webdriver.Chrome()
    last_available_year_in_database = find_last_year()
    if last_available_year_in_database is None:
        scrape_weather_data(driver, LAST_AVAILABLE_YEAR)
    else:
        year_of_db = datetime.strptime(
            last_available_year_in_database, "%Y-%m-%d %H:%M:%S"
        ).year
        if year_of_db < PAST_YEAR:
            scrape_weather_data(driver, year_of_db)
    driver.quit()
