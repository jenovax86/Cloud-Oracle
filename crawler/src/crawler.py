from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from database.db import insert_weather_records
from utils import generate_datetime, find_element
import constants


def parse_daily_weather_data(driver, year, month):
    weather_data_summary = []
    days_of_month = 0
    try:
        WebDriverWait(driver, constants.WEBDRIVER_TIMEOUT).until(
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
            time = find_element(section, "time")
            low_temperature = find_element(section, "tempLow low")
            high_temperature = find_element(section, "temp low")
            weather_data_summary.append(
                {
                    "date": generate_datetime(year, month, days_of_month, time),
                    "low_temperature": low_temperature,
                    "high_temperature": high_temperature
                }
            )

        return weather_data_summary

    except StaleElementReferenceException as error:
        raise ValueError(error)


def scrape_weather_data(connection, start_year, end_year):
    try:
        driver = webdriver.Chrome()
        yearly_data = []
        for year in range(start_year, end_year - 1, constants.DESCENDING_ORDER):
            for month in range(
                constants.FIRST_MONTH_OF_YEAR, constants.LAST_MONTH_OF_YEAR + 1
            ):
                driver.get(f"{constants.BASE_URL}?month={month}&year={year}")
                weather_data = parse_daily_weather_data(driver, year, month)
                yearly_data.extend(weather_data)
            insert_weather_records(connection, yearly_data)
    except Exception as error:
        raise ValueError(error)
    finally:
        driver.quit()
