from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import numpy as np
import pandas as pd

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
CITY = "tehran"
WEBDRIVER_TIMEOUT = 20


def previous_years():
    current_year = datetime.now().year
    years = list(range(current_year - 1, current_year - 6, -1))
    years.reverse()
    return years


def extract_date(date):
    return datetime.strptime(date.text, "%d %B %Y")


def clean_temperature_unit(temperature):
    temperature_value = temperature.replace("°C", "").strip()
    if temperature_value.isdigit():
        return int(temperature_value)


def clean_wind_unit(wind):
    wind_value = wind.replace("km/h", "").strip()
    if wind_value.isdigit():
        return int(wind_value)


def clean_humidity_unit(humidity):
    humidity_value = humidity.replace("%", "").strip()
    if humidity_value.isdigit():
        return int(humidity_value)


def mean_rounded(array):
    return np.round(np.mean(array)).astype(int)


def get_weather_specifics(driver):
    try:
        rows = WebDriverWait(driver, WEBDRIVER_TIMEOUT).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//table[@id = 'wt-his']//tbody/tr")
            )
        )
        temperatures, winds, humidities = [], [], []
        for row in rows:
            try:
                tds = row.find_elements(By.TAG_NAME, "td")
                temperature = clean_temperature_unit(tds[1].text)
                wind = clean_wind_unit(tds[3].text)
                humidity = clean_humidity_unit(tds[5].text)
                if not None in (temperature, wind, humidity):
                    temperatures.append(temperature)
                    winds.append(wind)
                    humidities.append(humidity)
            except StaleElementReferenceException:
                continue
        if all([temperatures, winds, humidities]):
            mean_temp = mean_rounded(temperatures)
            mean_wind = mean_rounded(winds)
            mean_humidity = mean_rounded(humidities)
        return mean_temp, mean_wind, mean_humidity
    except Exception as e:
        raise ValueError(e)


def select_days_dropdown(driver):
    weather_data = []
    select_element = driver.find_element(By.NAME, "start")
    select = Select(select_element)
    for option in select.options:
        date = extract_date(option)
        option_date_value = option.get_attribute("value")
        select.select_by_value(option_date_value)

        WebDriverWait(driver, WEBDRIVER_TIMEOUT).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//table[@id='wt-his']//tbody/tr")
            )
        )
        temp, wind, humidity = get_weather_specifics(driver)
        weather_data.append(
            {
                "country": COUNTRY,
                "city": CITY,
                "date": date,
                "temperature": temp,
                "wind": wind,
                "humidity": humidity,
            }
        )
    return weather_data


def scrape_weather_data():
    weather_scrapped_data = []
    driver = webdriver.Chrome()
    years = previous_years()
    for year in years:
        for _, month_number in MONTHS.items():
            driver.get(
                f"https://www.timeanddate.com/weather/{COUNTRY}/{CITY}/historic?month={month_number}&year={year}"
            )

            WebDriverWait(driver, WEBDRIVER_TIMEOUT).until(
                EC.presence_of_element_located((By.ID, "wt-his"))
            )
            WebDriverWait(driver, WEBDRIVER_TIMEOUT).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, "//table[@id = 'wt-his']//tbody/tr")
                )
            )
            weather_scrapped_result = select_days_dropdown(driver)
            if not weather_scrapped_data:
                weather_scrapped_data.extend(weather_scrapped_result)
    driver.quit()
    return pd.DataFrame(weather_scrapped_data)



scrape_weather_data()
